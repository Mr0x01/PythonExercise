# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from peewee import *

db = MySQLDatabase(
    "homesjp2",
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='',
    charset='utf8')

#建筑物对象
class HomesjpspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    bukkentype = scrapy.Field()  # 物件タイプ　房屋类型
    bukkentame = scrapy.Field()  # 物件名　名称
    bukkenurl = scrapy.Field()  # 物件URL
    bukkenid = scrapy.Field()  # 物件ID
    syozaichi = scrapy.Field()  # 所在地  地点
    koutsuu = scrapy.Field()  # 交通  周边交通
    nensu = scrapy.Field()  # 年数　建筑年数
    kaisu = scrapy.Field()  # 階数　建筑层
#建筑物模型
class Building(Model):
    id = AutoField()
    bukkenid = BigIntegerField(default=-1)
    bukkentype = CharField(default="")
    bukkentame = CharField(default="")
    bukkenurl = CharField(default="")
    syozaichi = CharField(default="")
    koutsuu = CharField(default="")
    nensu = CharField(default="")
    kaisu = CharField(default="")

    class Meta:
        database = db
#房间对象
class UnitItem(scrapy.Item):
    heyaid = scrapy.Field()
    bukkenid = scrapy.Field()
    floor = scrapy.Field()
    price = scrapy.Field()
    kyoueki = scrapy.Field()
    shikikin = scrapy.Field()
    reikin = scrapy.Field()
    housyou = scrapy.Field()
    shikihiki = scrapy.Field()
    layout = scrapy.Field()
    space = scrapy.Field()
    link = scrapy.Field()
#房间模型
class UnitModel(Model):
    id = AutoField()
    heyaid = BigIntegerField(default=-1)
    bukkenid = BigIntegerField(default=-1)
    floor = IntegerField(default=0)
    price = FloatField(default=0.0)
    kyoueki = FloatField(default=0.0)
    shikikin = FloatField(default=0.0)
    reikin = FloatField(default=0.0)
    housyou = FloatField(default=0.0)
    shikihiki = FloatField(default=0.0)
    layout = CharField(default="")
    space = FloatField(default=0.0)
    link = CharField(default="")
    syuyousaikoumen = CharField(default="")
    heyaid = BigIntegerField(default=-1)
    lat =  CharField(default="")
    lng =  CharField(default="")

    class Meta:
        database = db
#Cookie对象
class CookieItem(scrapy.Item):
    D_HID = scrapy.Field()
    D_IID = scrapy.Field()
    D_SID = scrapy.Field()
    D_UID = scrapy.Field()
    D_ZID = scrapy.Field()
    D_ZUID = scrapy.Field()
    TS01ec9519 = scrapy.Field()
#Cookie模型
class CookieModel(Model):
    id = AutoField()
    D_HID = CharField(default="")
    D_IID = CharField(default="")
    D_SID = CharField(default="")
    D_UID = CharField(default="")
    D_ZID = CharField(default="")
    D_ZUID = CharField(default="")
    TS01ec9519 = TextField(default="")
    status = IntegerField(default=0)
    class Meta():
        database = db

class UnitItemAdditional(scrapy.Item):
    syuyousaikoumen = scrapy.Field()
    heyaid = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
