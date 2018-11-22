import scrapy,logging,urllib,time
from renrenspider.items import *

class Renrenspider(scrapy.Spider):
    name = "renrenspider"
    def start_requests(self):
        return [
            scrapy.Request(
                url="http://3g.renren.com",
                method="GET",
                callback=self.login_page)
        ]

    def login_page(self, response):
        lbskey = response.css("div.form-inline>input[name=lbskey]::attr(value)").extract_first()  #取出登陆需要的值
        email = ""  #账号
        password = ""  #密码
        my_req = scrapy.FormRequest(
            url="http://3g.renren.com/login.do?autoLogin=true&&fx=0",
            method="POST",
            headers={
                "Referer": "http://3g.renren.com/home.do"
                },
            callback=self.login_callback,
            formdata={
                "origURL": r"/home.do",
                "lbskey": lbskey,
                "c": "",
                "pq": "",
                "appid": "",
                "ref": r"http://m.renren.com/q.do?null",
                "login": "",
                "email": email,
                "password": password
            },
            meta={
                "dont_redirect":True,
                "handle_httpstatus_list":[302]
            }
            )
        return my_req
    
    def login_callback(self,response):
        cookies = {}
        if response.status == 302:
            logging.info("检测到302")
            set_cookies = response.headers.getlist("Set-Cookie")
            for cookie in set_cookies:
                temp = cookie.decode("utf-8").split(";")[0].split("=")
                cookies[temp[0]] = temp[1]
            return [scrapy.Request(
                url="http://3g.renren.com/profile.do",
                cookies=cookies,
                callback=self.home_page,
                meta={
                    "cookies":cookies
                }
            )]
        elif response.text.find("请输入验证码") > -1:
            alxn = input("手动输入alxn：")
            cookies["alxn"] = alxn
            mt = input("手动输入mt：")
            cookies["mt"] = mt
            return [scrapy.Request(
                url="http://3g.renren.com/profile.do",
                cookies=cookies,
                callback=self.home_page,
                meta={
                    "cookies":cookies
                }
            )]

    def home_page(self,response):
        logging.info("主页")
        atags = response.css("div.sec > a")
        for atag in atags:
            link = atag.css("::attr(href)").extract_first()
            if link.find("friendlist.do")>-1:
                return response.follow(
                    url=link,
                    cookies=response.meta["cookies"],
                    callback=self.frinds_page,
                    meta={"cookies":response.meta["cookies"]}
                    )
    
    def frinds_page(self,response):
        logging.info("好友页") 
        friendlist = response.css("div.list div:not(.l)")
        # print(response.text)
        for friend in friendlist:
            friend_link = friend.css("a.p::attr(href)").extract_first()
            friend_id = urllib.parse.parse_qs(friend_link.split("?")[1])["id"][0]
            album_link = "http://3g.renren.com/album/wmyalbum.do?id={0}".format(friend_id)
            logging.info("好友ID：{0}".format(friend_id))
            yield scrapy.Request(
                url=album_link,
                cookies=response.meta["cookies"],
                callback=self.albumlist_page,
                meta={"cookies":response.meta["cookies"]}
            )
        next_page_link = response.css("div.l > a[title='下一页']::attr(href)").extract_first()
        if next_page_link !=None:
            yield scrapy.Request(
                url=next_page_link,
                cookies=response.meta["cookies"],
                callback=self.frinds_page,
                meta={"cookies":response.meta["cookies"]}
            )

    def albumlist_page(self,response):
        logging.info("相册列表页")
        album_list = response.css("a.p")
        if len(album_list) < 1:
            logging.info("没有相册")
        else:
            for album in album_list:
                album_url = album.css("::attr(href)").extract_first()
                yield scrapy.Request(
                    url=album_url,
                    cookies=response.meta["cookies"],
                    callback=self.each_album,
                    meta={"cookies":response.meta["cookies"]}
                )
            next_page_link = response.css("a[title='下一页']::attr(href)").extract_first()
            if next_page_link != None:
                yield scrapy.Request(
                    url=next_page_link,
                    cookies=response.meta["cookies"],
                    callback=self.albumlist_page,
                    meta={"cookies":response.meta["cookies"]}
                )

    def each_album(self,response):
        logging.info("相册页")
        img_list = response.css("div.list")[0].css("a")
        
        for img in img_list:
            img_url = img.css("::attr(href)").extract_first()
            yield scrapy.Request(
                url=img_url,
                cookies=response.meta["cookies"],
                callback=self.each_img,
                meta={"cookies":response.meta["cookies"]}
            )
        
        next_page_link = response.css("a[title='下一页']::attr(href)").extract_first()
        if next_page_link != None:
            yield scrapy.Request(
                url=next_page_link,
                cookies=response.meta["cookies"],
                callback=self.each_album,
                meta={"cookies":response.meta["cookies"]}
            )

    def each_img(self,response):
        logging.info("相片详情")
        img_item = RenrenspiderItem()
        friend_name = response.css("body > div.ssec > b > a::text").extract_first()
        img_item["friend_name"] = friend_name
        album_name = response.css("body > div:nth-child(14) > b::text").extract_first()
        img_item["album_name"] = album_name
        comment = ""
        try:
            comment = response.css("body > div:nth-child(15) > p:nth-child(3)")[0].css("::text").extract()[1].strip()
        except IndexError :
            comment = response.css("body > div:nth-child(15) > p:nth-child(3)*::text").extract_first().strip()
        img_item["img_comment"] = comment
        datetime = response.css("body > div:nth-child(15) > p.time::text").extract_first()
        if datetime == None and datetime == "":
            img_item["img_date"] = time.time_ns()
        else:
            img_item["img_date"] = datetime.replace("上传时间:","").strip()
        for taga in response.css("a"):
            if taga.css("::text").extract_first() == "下载":
                img_item["img_url"] = taga.css("::attr(href)").extract_first()
                break
        yield img_item

    

            


