# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *

db = MySQLDatabase(
    "renren.com",
    host="127.0.0.1",
    port=3306,
    user="root",
    passwd="",
    charset="utf8"
)

class RenrenspiderItem(scrapy.Item):
    img_id = scrapy.Field()
    friend_name = scrapy.Field()
    album_name = scrapy.Field()
    img_date = scrapy.Field()
    img_comment = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()

class RenrenspiderModel(Model):
    img_id = AutoField()
    friend_name = CharField(default="")
    album_name = CharField(default="")
    img_date = CharField(default="")
    img_comment = CharField(default="")
    img_url = CharField(default="")
    img_path = TextField(default="")
    status = CharField(default="")
    class Meta():
        database = db

class ErrorModel(Model):
    error_id = AutoField()
    error_msg = TextField(default="")
    class Meta():
        database = db