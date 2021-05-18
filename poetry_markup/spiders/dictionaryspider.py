from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from w3lib.html import remove_tags
from poetry_markup.items import DictItem
import os


class DictSpider(CrawlSpider):
    """
    Extract dictionaries from links specified in rules
    """
    custom_settings = {
        'ITEM_PIPELINES': {
            'poetry_markup.pipelines.DictSqlPipeline': 300
        }
    }
    name = "dictionary"
    root_url = "https://slovnyk.ua/"
    s2 = [0, 102, 106, 139, 103, 19, 109, 69, 21, 38, 130, 0, 59, 9, 15, 123, 75, 105, 128, 113, 220, 111, 145,
          104, 75, 75, 63, 49, 54, 66, 26, 0, 17, 32]
    start_urls = []
    for i in range(1, 34):
        for page in range(1, s2[i]):
            start_urls.append(os.path.join(root_url, f"index.php?s1={i}&s2={page}"))

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='cont_link']"),
             callback='parse'),
    )

    def parse(self, response, **kwargs):
        """
            Get items from given start_urls
            :param response: response from urls
            :return: scraped items
        """
        item_loader = ItemLoader(item=DictItem(), response=response)
        item_loader.default_input_processor = MapCompose(remove_tags)
        item_loader.add_xpath('stressed_word', '//div[@class="toggle-content"]//p//b//text()')
        yield item_loader.load_item()