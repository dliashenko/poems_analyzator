import logging
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import null

logger = logging.getLogger(__name__)


class PoemsSqlPipeline(object):
    """
    Pipeline for writing PoemsItem objects into sqlite database
    """

    def __init__(self):
        self.connection = sqlite.connect("../resources/poems.db")

    # noinspection PyUnusedLocal
    def open_spider(self, spider):
        """
        Create an poems table

        :param: the spider which was opened

        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS poems
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    author VARCHAR, 
                    title VARCHAR,
                    poem TEXT, 
                    publication_date VARCHAR)''')
        cursor.close()
        self.connection.commit()

    # noinspection PyUnusedLocal
    def process_item(self, item, spider):
        """
        Write item in a table poems

        :param item: the scraped item
        :param spider: the spider which scraped the item

        :return: item
        """
        author = item["author"][0]
        title = item["title"][0]
        poem = item["poem"][0]
        date = item["publication_date"][0] if ("publication_date" in item.keys()) else None
        cursor = self.connection.cursor()
        cursor.execute("SELECT * FROM poems WHERE poem = ?", item["poem"])
        result = cursor.fetchone()
        cursor.close()
        self.connection.commit()
        if result:
            logger.info("Item is already in database : " % item)
        else:
            cursor = self.connection.cursor()
            cursor.execute('''INSERT into poems 
                           (author, title, poem, publication_date)
                            VALUES (?,?,?,?)''',
                           (author, title, poem, date))
            cursor.close()
            self.connection.commit()
            logger.info("Item stored : " % item)
        return item

    # noinspection PyUnusedLocal
    def close_spider(self, spider):
        """
        Closes the sqlite connection

        :param spider: the spider which was closed
        """
        self.connection.close()


class DictSqlPipeline(object):
    """
    Pipeline for writing DictItem objects into sqlite database
    """

    def __init__(self):
        self.connection = sqlite.connect("../resources/dictionary.db")

    def word_from_stressed_word(self, stressed_word):
        return stressed_word.replace("*", "") if stressed_word is not None else None

    # noinspection PyUnusedLocal
    def open_spider(self, spider):
        """
        Create an dictionary table

        :param: the spider which was opened

        :return: None
        """
        cursor = self.connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS dictionary
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                    word VARCHAR, 
                    stressed_word VARCHAR)''')
        cursor.close()
        self.connection.commit()

    # noinspection PyUnusedLocal
    def process_item(self, item, spider):
        """
        Write item in a table dictionary

        :param item: the scraped item
        :param spider: the spider which scraped the item

        :return: item
        """
        stressed_word = item["stressed_word"][0] if ("stressed_word" in item.keys()) else None
        word = self.word_from_stressed_word(stressed_word)
        cursor = self.connection.cursor()
        if stressed_word is not None:
            cursor.execute("SELECT * FROM dictionary WHERE stressed_word = ?", item["stressed_word"])
            result = cursor.fetchone()
            cursor.close()
            self.connection.commit()
            if result:
                logger.info("Item is already in database : " % item)
            else:
                cursor = self.connection.cursor()
                cursor.execute('''INSERT into dictionary(word,stressed_word)
                               VALUES(?, ?)''',
                               (word, stressed_word))
                cursor.close()
                self.connection.commit()
                logger.info("Item stored : " % item)
        return item

    # noinspection PyUnusedLocal
    def close_spider(self, spider):
        """
        Closes the sqlite connection

        :param spider: the spider which was closed
        """
        self.connection.close()

