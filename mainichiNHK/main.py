import requests, time, json, pymongo, m3u8, os
from model import News

uri = "mongodb://root:1q2w#E$R@10.20.10.98/mainichiNHK?authSource=admin"
client = pymongo.MongoClient(uri)
db = client.mainichiNHK
news_collect = db.News


def get(url,is_stream=False):
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"
    return requests.request(
        "GET", url, headers={"user-agent": user_agent}, timeout=60,stream=is_stream)


#step1 Fetching json data from api
try:
    ts = time.time()
    news_list = get(
        "https://www3.nhk.or.jp/news/easy/news-list.json?_={0}".format(ts))
except requests.exceptions.RequestException as err:
    raise err

#step2 Load json and stored it in mongodb
news_list_json = json.loads(news_list.text)[0]
for date in news_list_json:
    news_today = news_list_json[date]
    for news in news_today:
        temp_news = News()
        temp_news.__dict__ = news
        news_count = news_collect.find(
            {
                "news_id": temp_news.news_id
            }
        ).count()
        if news_count == 0:
            news_collect.insert_one(news)
            news_url = "https://www3.nhk.or.jp/news/easy/{0}/{0}.html".format(temp_news.news_id)
            master_m3u8 = m3u8.load("https://nhks-vh.akamaihd.net/i/news/easy/{0}.mp4/master.m3u8".format(temp_news.news_id))
            index_0_a_m3u8_url = master_m3u8.playlists[0].uri
            if os.path.exists("media_files")==False:
                os.mkdir("media_files")
            os.system("ffmpeg.exe -i \"{0}\" -c copy media_files/\"{1}\".mp4".format(index_0_a_m3u8_url,temp_news.news_id))
            # index_0_a_m3u8 = m3u8.load(master_m3u8.playlists[0].uri)
            # for file in index_0_a_m3u8.files:
            #     file_name = file.split("/")[-1].split("?")[0]
            #     rep = get(file,True)
            #     with open(file_name,"wb") as f:
            #         for chunk in rep.iter_content(chunk_size=1024):
            #             if chunk:
            #                 f.write(chunk)



        
        
