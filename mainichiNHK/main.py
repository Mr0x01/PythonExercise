import requests
import time
import json
import codecs
import pymongo
import m3u8
import os
from bs4 import BeautifulSoup
from utils.mongo_util import MongoUtil
from model import News

client = MongoUtil().client
db = client.mainichiNHK
news_collect = db.News

my_proxies = {
    "http": "127.0.0.1:1080",
    "https": "127.0.0.1:1080",
}


def get(url, proxy=my_proxies, timeout=60, is_stream=False):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    r = requests.request(
        "GET",
        url,
        headers={"user-agent": user_agent},
        timeout=60,
        stream=is_stream,
        verify=False,
        proxies=proxy
    )
    r.encoding = 'UTF-8 BOM'
    return r


# step1 Fetching json data from api
try:
    ts = time.time()
    news_list = get(
        "https://www3.nhk.or.jp/news/easy/news-list.json?_={0}".format(ts)
    )
except requests.exceptions.RequestException as err:
    raise err

# step2 Load json and stored it in mongodb
news_list_str = news_list.text
if news_list_str.startswith(u'\ufeff'):
    news_list_str = news_list_str.encode('utf8')[3:]
news_list_json = json.loads(news_list_str)[0]
my_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
for date in news_list_json:
    news_today = news_list_json[date]
    for news in news_today:
        temp_news = News()
        temp_news.__dict__ = news
        news_count = news_collect.find({"news_id": temp_news.news_id}).count()
        if news_count == 0:
            news_url = "https://www3.nhk.or.jp/news/easy/{0}/{0}.html".format(
                temp_news.news_id)
            temp_html = get(news_url)
            temp_html.encoding = "utf-8"
            soup = BeautifulSoup(temp_html.text)
            article_html = soup.select_one("#js-article-body")
            article_text = article_html.text
            news["news_web_url"] = news_url
            news["article_html"] = str(article_html)
            news["article_text"] = str(article_text).replace("\n", "")
            if news["article_text"].find("近平") > -1 or news["article_text"].find("毛沢東") > -1 or news["article_text"].find("台湾") > -1 or news["article_text"].find("北朝鮮") > -1 or news["article_text"].find("ファーウェイ") > -1:
                continue
            news_dict_url = "https://www3.nhk.or.jp/news/easy/{0}/{0}.out.dic?date={1}".format(
                news["news_id"], time.time())
            news_dict = get(news_dict_url).text
            news["news_dict"] = news_dict
            news["insert_time"] = my_time

            try:
                img = get(news["news_web_image_uri"], timeout=10)
                if img.text.find("記事が見つかりませんでした") == -1:
                    open("media_files\\" + news["news_id"] + ".jpg",
                         "wb").write(img.content)
                    news["news_web_image_uri"] = news["news_id"] + ".jpg"
                else:
                    news["news_web_image_uri"] = "default.jpg"

            except Exception as e:
                news["news_web_image_uri"] = "default.jpg"
                pass

            master_m3u8 = m3u8.load(
                "https://nhks-vh.akamaihd.net/i/news/easy/{0}.mp4/master.m3u8".format(temp_news.news_id))
            index_0_a_m3u8_url = master_m3u8.playlists[0].uri
            if os.path.exists("media_files") == False:
                os.mkdir("media_files")
            os.system("ffmpeg.exe -i \"{0}\" -c copy media_files/\"{1}\".mp4".format(
                index_0_a_m3u8_url, temp_news.news_id))
            news_collect.insert_one(news)
