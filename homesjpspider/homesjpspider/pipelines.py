# -*- coding: utf-8 -*-
from homesjpspider.items import *
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class HomesjpspiderPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, HomesjpspiderItem):
            building = Building(
                bukkentype=item["bukkentype"],
                bukkentame=item["bukkentame"],
                bukkenurl=item["bukkenurl"],
                bukkenid=item["bukkenid"],
                syozaichi=item["syozaichi"],
                koutsuu=item["koutsuu"],
                nensu=item["nensu"],
                kaisu=item["kaisu"],
            )
            building.save()
        if isinstance(item, UnitItem):
            unitModel = UnitModel(
                bukkenid=item["bukkenid"],
                floor=item["floor"],
                price=item["price"],
                kyoueki=item["kyoueki"],
                shikikin=item["shikikin"],
                reikin=item["reikin"],
                housyou=item["housyou"],
                shikihiki=item["shikihiki"],
                layout=item["layout"],
                space=item["space"],
                link=item["link"]
            )
            unitModel.save()
        if isinstance(item,CookieItem):
            cookieModel = CookieModel(
                D_HID = item["D_HID"],
                D_IID = item["D_IID"],
                D_SID = item["D_SID"],
                D_UID = item["D_UID"],
                D_ZID = item["D_ZID"],
                D_ZUID = item["D_ZUID"],
                TS01ec9519 = item["TS01ec9519"]
            )
            cookieModel.save()
        return item
