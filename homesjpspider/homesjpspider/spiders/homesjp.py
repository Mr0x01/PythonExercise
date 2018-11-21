import scrapy
import urllib
import logging
from homesjpspider.utils.homesjp_util import Homesjp_Util
from homesjpspider.items import *
import json
import urllib


class Homesjp(scrapy.Spider):
    name = "homesjpspider"

    #start_urls = ["https://www.homes.co.jp/chintai/tokyo/list/"]

    def start_requests(self):
        _cookies = {}
        cookieModel = CookieModel.get(CookieModel.status == 0)
        CookieModel.update(status=1).where(
            CookieModel.id == cookieModel.id).execute()
        _cookies["D_HID"] = cookieModel.D_HID
        _cookies["D_IID"] = cookieModel.D_IID
        _cookies["D_SID"] = cookieModel.D_SID
        _cookies["D_UID"] = cookieModel.D_UID
        _cookies["D_ZID"] = cookieModel.D_ZID
        _cookies["D_ZUID"] = cookieModel.D_ZUID
        _cookies["TS01ec9519"] = cookieModel.TS01ec9519
        yield scrapy.Request(
            url="https://www.homes.co.jp/chintai/tokyo/23ku/list/",
            headers={
                "Referer": "https://www.homes.co.jp/chintai/tokyo/23ku/list/"
            },
            method="GET",
            cookies=_cookies,
            callback=self.my_parse,
            meta={"dont_redirect": True},
            dont_filter=True)

    def my_parse(self, response):
        cookie_list = response.headers.getlist("Set-Cookie")
        _cookies = {}
        for index in range(0, len(cookie_list)):
            temp_cookie = cookie_list[index].decode("utf-8").split(";")[0]
            key = temp_cookie.split("=")[0]
            value = temp_cookie.split("=")[1]
            _cookies[key] = value
        logging.info("{0}:{1}".format(key, value))
        list = response.css("div.mod-mergeBuilding--rent")
        for item in list:
            # 上半部分，建筑概要
            bukkentype = item.css("span.bType::text").extract_first()
            bukkentame = item.css("span.bukkenName::text").extract_first()
            bukkenurl = item.css(".moduleHead a::attr(href)").extract_first()
            bukkenid = bukkenurl.split("-")[1].replace("/", "")
            syozaichi = item.css(
                "div.bukkenSpec > table > tbody > tr:nth-child(1) > td::text"
            ).extract_first()
            koutsuu = item.css(
                "div.bukkenSpec > table > tbody > tr:nth-child(2) > td::text"
            ).extract_first()
            nensutokaisu = str(
                item.
                css("div.bukkenSpec > table > tbody > tr:nth-child(3) > td::text"
                    ).extract_first()).split("/")
            nensu = nensutokaisu[0].strip()
            kaisu = nensutokaisu[1].strip()
            home_itme = HomesjpspiderItem()
            home_itme["bukkentype"] = bukkentype.strip()
            home_itme["bukkenurl"] = bukkenurl.strip()
            home_itme["bukkenid"] = bukkenid.strip()
            home_itme["bukkentame"] = bukkentame.strip()
            home_itme["syozaichi"] = syozaichi.strip()
            home_itme["koutsuu"] = koutsuu.strip()
            home_itme["nensu"] = nensu.strip()
            home_itme["kaisu"] = kaisu.strip()
            yield home_itme

            # 下半部分，房间详情
            unit_summary_list = item.css("table.unitSummary>tbody>tr")
            for tr in unit_summary_list[1:len(unit_summary_list)]:
                tds = tr.css("td")
                unit = UnitItem()
                unit["bukkenid"] = home_itme["bukkenid"]
                unit["floor"] = tds.css(
                    ".floar::text").extract_first().strip().replace("階", "")
                price = float(tds.css(".price *::text").extract_first()) * 10000
                unit["price"] = price
                unit["kyoueki"] = tds.css(
                    ".kyoueki::text").extract_first().strip()
                cost = tds.css(".cost::text").extract_first().split("/")
                unit["shikikin"] = cost[0].strip()
                unit["reikin"] = cost[1].strip()
                unit["housyou"] = cost[2].strip()
                unit["shikihiki"] = cost[3].strip()
                unit["layout"] = tds.css(
                    ".layout::text").extract_first().strip()
                unit["space"] = float(tds.css(".space::text").extract_first().strip().replace("m²",""))
                unit["link"] = tds.css(
                    ".detail a::attr(href)").extract_first().strip()
                yield unit
            # 翻页
            if response.css(".nextPage")[0] != None:
                next_page_url = response.css(".nextPage a")[0]
                yield response.follow(
                    next_page_url,
                    cookies=_cookies,
                    meta={"dont_redirect": True},
                    callback=self.my_parse)
