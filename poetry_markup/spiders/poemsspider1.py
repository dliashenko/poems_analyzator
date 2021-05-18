from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from poetry_markup.items import Poem1Item
import os


class PoemSpider(CrawlSpider):
    """
    Extract all poems information(title,author,published date,poem) from links specified in rules
    """
    name = "poems1"

    custom_settings = {
        'ITEM_PIPELINES': {
            'poetry_markup.pipelines.PoemsSqlPipeline': 300
        }
    }

    root_url = "https://www.ukrlib.com.ua/books"
    ids = [13, 5, 260, 199]
    pages = [8, 11, 2, 1]
    start_urls = []
    for i in range(0, 4):
        for page in range(0, pages[i]+1):
            start_urls.append(os.path.join(root_url, f"author.php?id={ids[i]}&page={page}"))

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='list ']//li//a"),
             callback='parse'),
        Rule(LinkExtractor(restrict_xpaths="//ul[@class='list']//li//a"),
             callback='parse'),
    )

    def parse(self, response, **kwargs):
        """
            Get items from given start_urls
            :param response: response from urls
            :return: scraped items
        """
        item_loader = ItemLoader(item=Poem1Item(), response=response)
        item_loader.default_input_processor = MapCompose(remove_tags)
        item_loader.add_xpath('title', '//div[@class="page-title "]//h1/text()')
        item_loader.add_xpath('publication_date', '//article[@class="prose"]/text()')
        item_loader.add_xpath('author', '//div[@class="page-title "]//h2/text()')
        item_loader.add_xpath('poem', '//article[@class="prose"]/text()')
        yield item_loader.load_item()
