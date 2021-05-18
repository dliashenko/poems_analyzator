# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import re
import scrapy
from itemloaders.processors import Compose

vowels = ['у', 'е', 'і', 'о', 'я', 'и', 'ю', 'а', 'ї', 'є']


def to_clean(value):
    """
    Remove all unnecessary characters from ArticlesItem author and join into a single string
    :param value: values to be processed
    :type: list
    :return: Formatted string value
    """
    leng = len(value)
    if any(char.isdigit() for char in value[leng - 1]):
        return [re.sub(r"[*\s\n]{2,}", "\n", "".join(value[:-1]).strip())]
    else:
        return [re.sub(r"[*\s\n]{2,}", "\n", "".join(value).strip())]


def clean(value):
    """
    Remove all unnecessary characters from ArticlesItem date and turn in into datetime value
    :param value: values to be processed
    :type: list
    :return: datetime
    """
    return [re.sub(r'[*_]', '', "\n".join(value)).strip()]


def get_date(value):
    leng = len(value)
    date = re.sub(r"[\s]{2,}", "\n", value[leng - 1]).strip()
    if any(char.isdigit() for char in date):
        return [date]


def nagolos(value):
    word = [i.lower() for i in value if len(value) > 1][:3]
    if len(word[0]) == 1 and word[0] in vowels:
        word.insert(1, '*')
    elif len(word[1]) == 1 and word[1] in vowels:
        word.insert(2, '*')
    return ["".join(word)]


# def simple_word(value):
#     return "".join([i.lower() for i in value][:3])


class Poem1Item(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    poem = scrapy.Field(
        output_processor=Compose(to_clean)
    )
    publication_date = scrapy.Field(
        output_processor=Compose(get_date)
    )


class PoemItem(scrapy.Item):
    author = scrapy.Field()
    title = scrapy.Field()
    poem = scrapy.Field(
        output_processor=Compose(clean)
    )
    publication_date = scrapy.Field()


class DictItem(scrapy.Item):
    stressed_word = scrapy.Field(
        output_processor=Compose(nagolos)
    )
