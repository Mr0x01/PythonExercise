# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Mm131SpiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    ImgName = scrapy.Field()
    ImgUrl = scrapy.Field()
    ImgReferer = scrapy.Field()
    ImgPath = scrapy.Field()
    pass
