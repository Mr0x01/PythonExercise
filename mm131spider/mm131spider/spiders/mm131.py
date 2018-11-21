# -*- coding: utf-8 -*-

import scrapy
from mm131spider.mm131spider.items import Mm131SpiderItem

class Mm131spider(scrapy.Spider):
    name = "mm131spider"
    allowed_domain = ["mm131.com"]
    start_urls = ["http://www.mm131.com/mingxing"]

    def parse(self, response):
        list = response.css(".list-left dd:not(.page)")
        for img in list:
            #图集名称
            album_name = img.css("a::text").extract_first()
            #图集地址 后面用作referer
            album_url = str(img.css("a::attr(href)").extract_first())
            print(album_name, album_url)
            next_url = response.css(".page-en:nth-last-child(2)::attr(href)").extract_first()
            if next_url is not None:
                yield response.follow(next_url, callback=self.parse)
            yield scrapy.Request(album_url, callback=self.img)

    def img(self, response):
        item = Mm131SpiderItem()
        item["ImgReferer"] = response.url
        item["ImgUrl"] = response.css(".content-pic img::attr(src)").extract()
        item["ImgName"] = response.css(".content h5::text").extract_first()
        yield item
        next_url = response.css(
            ".page-ch:last-child::attr(href)").extract_first()
        if next_url is not None:
            yield response.follow(next_url, callback=self.img)
