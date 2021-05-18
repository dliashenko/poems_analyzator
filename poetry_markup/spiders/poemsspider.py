from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from poetry_markup.items import PoemItem
import os


class PoemsSpider(CrawlSpider):
    """
    Extract all poems information(title,author,published date,poem) from links specified in rules
    """
    name = "poems"

    custom_settings = {
        'ITEM_PIPELINES': {
            'poetry_markup.pipelines.PoemsSqlPipeline': 300
        }
    }

    root_url = "http://ukrlit.org/"
    start_urls = [root_url,
                  os.path.join(root_url, "zerov_mykola_kostiantynovych/tvory"),
                  os.path.join(root_url, "symonenko_vasyl_andriiovych/tvory")]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='''//div[@class='works']//div[@class='works-list'][1]
        //ul//li[@class='works-list__item']'''),
             callback='parse'),
    )

    def parse(self, response, **kwargs):
        """
            Get items from given start_urls
            :param response: response from urls
            :return: scraped items
        """
        item_loader = ItemLoader(item=PoemItem(), response=response)
        item_loader.default_input_processor = MapCompose(remove_tags)
        item_loader.add_xpath('title', '//div[@class="work__topper work__topper_pad"]//h2[@class="h2"]/text()')
        item_loader.add_xpath('publication_date', 'normalize-space(//article[@class="tvir"]//p//small//i/text())')
        item_loader.add_xpath('author', '''normalize-space(//div[@class="work-item__title"]//h3[@class = "h4"]|
        //a[@class="work-item__author"]/text())''')
        item_loader.add_xpath('poem', '//article[@class="tvir"]//p/text()')
        yield item_loader.load_item()
