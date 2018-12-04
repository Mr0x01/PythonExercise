# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import logging
from homesjpspider.items import *
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message


class HomesjpspiderSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class HomesjpspiderDownloaderMiddleware(RetryMiddleware):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        #return None
        if spider.name == "homesjpspider":
            request.headers["referer"] = "https://www.homes.co.jp/chintai/tokyo/city/"
            if request.meta.get("Edited",-1) == 1:
                logging.error("Cookie将进行更换")
                _cookies = {}
                cookieModel = CookieModel.get(CookieModel.status == 0)
                if cookieModel != None:
                    CookieModel.update(status=1).where(
                        CookieModel.id == cookieModel.id).execute()
                    _cookies["D_HID"] = cookieModel.D_HID
                    _cookies["D_IID"] = cookieModel.D_IID
                    _cookies["D_SID"] = cookieModel.D_SID
                    _cookies["D_UID"] = cookieModel.D_UID
                    _cookies["D_ZID"] = cookieModel.D_ZID
                    _cookies["D_ZUID"] = cookieModel.D_ZUID
                    _cookies["TS01ec9519"] = cookieModel.TS01ec9519
                    request.cookies = _cookies
                else:
                    logging.error("Cookie不够用了。。")

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        if spider.name == "homesjpspider":
            request.replace(dont_filter=True)
            if response.text.find("distil_r_captcha.html?requestId=") > -1:
                request.meta["Edited"] = 1
                reason = response_status_message(response.status)
                return self._retry(request, reason, spider) or response  # 重试
            else:
                return response
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
