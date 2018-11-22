# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RenrenspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    friend_name = scrapy.Field()
    album_name = scrapy.Field()
    img_date = scrapy.Field()
    img_comment = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()
