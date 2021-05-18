import pandas as pd
from sqlite3 import dbapi2 as sqlite
import pymorphy2
import re
import yaml
from ast import literal_eval
from poetry_markup.items import vowels


def get_tokens(raw_poems):
    poems_lines = [poem[1].split("\n") for poem in raw_poems]
    line_tokens = [line.split() for poem in poems_lines for line in poem]
    raw_tokens = [word.lower().replace("’", "'") for line in line_tokens for word in line]
    tokens = [re.match(r"[а-яА-ЯіІїЇєЄґҐ'-]*", token).group() for token in raw_tokens]
    return set(tokens)


def get_stressed_words_positions(words):
    morph = pymorphy2.MorphAnalyzer(lang='uk')
    normalized_words = [morph.parse(word)[0].normal_form for word in words]
    connection = sqlite.connect("../resources/databases/dictionary.db")
    dict_words = {}
    for word in normalized_words:
        if word != "":
            value_from_dict = pd.read_sql_query('SELECT stressed_word FROM dictionary WHERE word = "' + word
                                                + '"', connection)
            if not value_from_dict.empty:
                dict_words[word] = value_from_dict.to_numpy()[0][0]
    stress_pos = {key: value.find("*") for (key, value) in dict_words.items()}
    return stress_pos


def get_marked_up_poems(stress_pos, raw_poems):
    poems_lines = [[poem[0], poem[1].split("\n")] for poem in raw_poems]
    morph = pymorphy2.MorphAnalyzer(lang='uk')
    marked_up_poems = []
    for poem in poems_lines:
        marked_up_poem = []
        for line in poem[1]:
            marked_line = []
            for word in line.split():
                search_word = re.match(r"[а-яА-ЯіІїЇєЄґҐ'-]*", word).group().lower()
                normal_form = morph.parse(search_word)[0].normal_form
                has_vowel = re.findall(r"[уеоїіаєяию]", word)
                if normal_form in stress_pos.keys():
                    pos = stress_pos[normal_form]
                    word = search_word[:pos] + "*" + search_word[pos:]
                elif len(has_vowel) == 1:
                    pos = word.find(has_vowel[0])
                    word = word[:pos + 1] + "*" + word[pos + 1:]
                marked_line.append(word)
            marked_up_line = " ".join(marked_line)
            marked_up_poem.append(marked_up_line)
        marked_up_poems.append([poem[0], marked_up_poem])
    return marked_up_poems


def mark_up_meters(marked_up_poems):
    poems_patterns = []
    for poem in marked_up_poems:
        poem_patterns = []
        for line in poem[1]:
            line_pattern = ""
            for i, symbol in enumerate(line):
                if symbol in vowels:
                    if (line + " ")[i + 1] == "*":
                        line_pattern += "u"
                    else:
                        line_pattern += "-"
            poem_patterns.append(line_pattern)
        poems_patterns.append([poem[0], poem_patterns])
    return poems_patterns


def guess_meter(poem_patterns):
    with open("../resources/stress/meter_patterns.txt", "r") as file:
        meters = literal_eval(file.read())

    def line_analyze(line):
        ind = 0
        counter = {key: 0 for key in meters.keys()}
        for ikt in line:
            for key in counter.keys():
                if meters[key][ind] == ikt:
                    counter[key] += 1
            ind += 1
            if ind == 6:
                ind = 0
        return counter

    poems_meters = []
    for pattern in poem_patterns:
        poem_meters = []
        feets_sum = 0
        for line in pattern[1].split("\n"):
            line_meters = line_analyze(line)
            feet = len(re.findall(r"u{1}", line))
            if feet == 0: feet = 1
            koef = len(line) / feet
            feets_sum += feet
            edge2 = 2.3
            edge3 = 2.5
            for meter in line_meters.keys():
                if koef < edge2:
                    if (meter == "ямб") | (meter == "хорей"):
                        line_meters[meter] *= 1.5
                elif koef > edge3:
                    if (meter == "дактиль") | (meter == "анапест") | (meter == "амфібрахій"):
                        line_meters[meter] *= 1.5
                if line_meters[meter] == max(line_meters.values()):
                    poem_meters.append(meter)
        feet_num = round(feets_sum / len(pattern[1].split("\n")))
        out_meter = final_meter(poem_meters)
        for meter in out_meter:
            if out_meter[meter] == max(out_meter.values()):
                poems_meters.append([pattern[0], out_meter, meter, feet_num])
    return poems_meters


def final_meter(poem_meters):
    scores = {}
    for meter in poem_meters:
        if meter in scores.keys():
            scores[meter] += 1
        else:
            scores[meter] = 1
    return scores


def dict_to_str(dictionary):
    dict_string = ""
    for key in dictionary.keys():
        dict_string += key + ":" + str(dictionary[key]) + "\n"
    return dict_string


if __name__ == "__main__":
    conn = sqlite.connect("../resources/databases/poems.db")
    # poems = pd.read_sql_query("SELECT id, poem FROM poems", conn)
    # poems_texts = poems.to_numpy()
    # poems_words = get_tokens(poems_texts)
    # stress_positions = get_stressed_words_positions(poems_words)
    # with open("stress.txt", "w") as f:
    #     for stress in stress_positions.items():
    #         f.write(str(stress) + "\n")
    # with open("../resources/stress/stress.txt", "r") as f:
    #     stress_positions = literal_eval(f.read())
    # stressed_poems = get_marked_up_poems(stress_positions, poems_texts)
    # poems_patterns = mark_up_meters(stressed_poems)
    patterns = pd.read_sql_query("SELECT poem_id, pattern FROM patterns", conn)
    meters = guess_meter(patterns.to_numpy())
    cursor = conn.cursor()
    for meter in meters:
        cursor.execute("UPDATE patterns SET guesses = '" + dict_to_str(meter[1]) +
                       "', meter = '" + meter[2] + "', feet_number = '" + str(meter[3]) +
                       "' WHERE poem_id = " + str(meter[0]))
    cursor.close()
    conn.commit()
    conn.close()
