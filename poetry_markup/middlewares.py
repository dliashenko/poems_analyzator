# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class DiplomaPoetrySpiderMiddleware:
    """
    Automatically generated class by Scrapy
    """

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """
        This method is used by Scrapy to create spiders.
        :param cls: Middleware object
        :param crawler: Current spider
        :return:
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # noinspection PyUnusedLocal,PyUnusedLocal
    def process_spider_input(self, response, spider):
        """
        Called for each response that goes through the spider
        middleware and into the spider.
        :param response: Current response
        :param spider: Current spider
        :return: None
        """
        return None

    # noinspection PyUnusedLocal,PyUnusedLocal
    def process_spider_output(self, response, result, spider):
        """
        Called with the results returned from the Spider, after
        it has processed the response.
        :param response: Processed response
        :param result: Spider results
        :param spider: Current spider
        :return: item objects
        """
        for i in result:
            yield i

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def process_spider_exception(self, response, exception, spider):
        """
        Called when a spider or process_spider_input() method (from other spider middleware) raises an exception.
        :param response: Current spider response
        :param exception: Occurred exception
        :param spider: Current spider
        :return: None
        """
        return None

    # noinspection PyUnusedLocal
    def process_start_requests(self, start_requests, spider):
        """
        Called with the start requests of the spider, and works
        similarly to the process_spider_output() method, except
        that it doesn’t have a response associated.
        :param start_requests: Start requests of current spider
        :param spider: Current spider
        :return: requests
        """
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        """
        Tell which spider is opened
        :param spider: Current spider
        :return: None
        """
        spider.logger.info('Spider opened: %s' % spider.name)


# noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,PyUnusedLocal,
# noinspection PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic,PyMethodMayBeStatic
class DiplomaPoetryDownloaderMiddleware:
    """
        Automatically generated class by Scrapy
    """

    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        """
        This method is used by Scrapy to create spiders.
        :param cls: Middleware object
        :param crawler: Current spider
        :return:
        """
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    # noinspection PyUnusedLocal,PyUnusedLocal
    def process_request(self, request, spider):
        """
        Called for each request that goes through the downloader middleware.
        :param request: Current processed request
        :param spider: Current spider
        :return: None
        """
        return None

    # noinspection PyUnusedLocal,PyUnusedLocal
    def process_response(self, request, response, spider):
        """
        Called with the response returned from the downloader.
        :param request: Processed request
        :param response: Processed response
        :param spider: Current spider
        :return: Response object
        """
        return response

    # noinspection PyUnusedLocal,PyUnusedLocal,PyUnusedLocal
    def process_exception(self, request, exception, spider):
        """
         Called when a download handler or a process_request()
        (from other downloader middleware) raises an exception.
        :param request: Processed request
        :param exception: Occurred exception
        :param spider: Current spider
        :return: None
        """
        return None

    def spider_opened(self, spider):
        """
        Tell which spider is opened
        :param spider: Current spider
        :return: None
        """
        spider.logger.info('Spider opened: %s' % spider.name)
