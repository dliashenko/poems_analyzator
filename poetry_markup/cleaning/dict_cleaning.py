from sqlite3 import dbapi2 as sqlite
import re


def clean_unwanted_symbols(conn):
    def delete_unwanted(symbol):
        cursor = conn.cursor()
        cursor.execute('SELECT word,stressed_word FROM dictionary WHERE word LIKE "%' + symbol + '%"')
        words = cursor.fetchall()
        cursor.close()
        cursor = conn.cursor()
        cursor.execute('DELETE FROM dictionary WHERE stressed_word LIKE "%' + symbol + '%"')
        cursor.close()
        for word_tuple in words:
            position = word_tuple[0].find(symbol)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO dictionary(word, stressed_word) '
                           'VALUES (?,?)',
                           (word_tuple[0][:position], word_tuple[1][:position+1]))
            cursor.close()
    unwanted_list = ["^", ":", ",", "@", " ", "1", "2", "**", "(", "["]
    for symbol in unwanted_list:
        delete_unwanted(symbol)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM dictionary WHERE stressed_word NOT LIKE "%*%"')
    cursor.close()


def clean_poems_date(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT publication_date,id FROM poems")
    dates = cursor.fetchall()
    cursor.close()

    for date_tuple in dates:
        date = re.search(r"\d{4}", date_tuple[0]if date_tuple[0] is not None else '')
        if date is not None:
            date = date.group()
            cursor = conn.cursor()
            cursor.execute("UPDATE poems SET year = ? WHERE id = ?", (date, date_tuple[1]))
            cursor.close()


if __name__ == "__main__":
    connection = sqlite.connect("../resources/databases/dictionary.db")
    clean_unwanted_symbols(connection)
    connection.commit()
    connection.close()
    connection = sqlite.connect("../resources/databases/poems.db")
    clean_poems_date(connection)
    connection.commit()
    connection.close()
