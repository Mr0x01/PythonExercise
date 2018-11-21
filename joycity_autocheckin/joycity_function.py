import json
import time as t

import requests

from module import CheckLog


#日志方法
def log(logstr: "日志内容"):
    present_time = t.strftime("%Y-%m-%d %H:%M:%S", t.localtime())
    print("[{}]{}".format(present_time, logstr))


#登陆方法
def login(username, password):
    url = "https://m.mallcoo.cn/api/user/user/Login?_type=2"
    token = ""
    #请求头参数
    my_headers = {
        "User-Agent":
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89",
        "Accept":
        "application/json; charset=utf-8",
        "Referer":
        "https://m.mallcoo.cn/a/user/10025/Checkin/Detail?_type=2&_appId=12&_pjcId=15047",
        "Content-Type":
        "text/plain",
        "X-Requested-With":
        "XMLHttpRequest",
        "Accept-Encoding":
        "gzip, deflate",
        "Accept-Language":
        "en-us"
    }
    #请求参数
    my_para = {
        "MallID": 10025,
        "Mobile": username,
        "SNSType": 0,
        "Pwd": password,
        "VCode": "",
        "LoginType": 1,
        "OauthID": None,
        "Keyword": "",
        "Scene": 4,
        "GraphicType": 2,
        "Header": {
            "Token": None
        }
    }

    try:
        log("发起请求..")
        response = requests.post(url, json=my_para, headers=my_headers)
        if response.text.find("Token") > -1:
            response_json = response.json()
            token = response_json["d"]["Token"].rstrip()
            checklog = CheckLog()
            checklog.msg = token
            checklog.result = "OK"
            checklog.date = t.time
            log("登陆成功，Token为[" + token + "]")
            return checklog
        else:
            if response.text.find("账户名与密码不匹配") > -1:
                checklog = CheckLog()
                checklog.result = "ERROR"
                checklog.msg = "密码错误"
                checklog.date = t.time
                log("登陆失败，用户名密码不匹配。")
                return checklog
    except Exception as e:
        checklog = CheckLog()
        checklog.result = "ERROR"
        checklog.msg = e
        checklog.date = t.time
        raise e


def check_in(token):
    url = "https://m.mallcoo.cn/api/user/User/Checkin?_type=2"
    #请求头参数
    my_headers = {
        "User-Agent":
        "Mozilla/5.0 (iPhone; CPU iPhone OS 10_3_2 like Mac OS X) AppleWebKit/603.2.4 (KHTML, like Gecko) Mobile/14F89",
        "Accept":
        "application/json; charset=utf-8",
        "Referer":
        "https://m.mallcoo.cn/a/user/10025/Checkin/Detail?_type=2&_appId=12&_pjcId=15047",
        "Content-Type":
        "text/plain",
        "X-Requested-With":
        "XMLHttpRequest",
        "Accept-Encoding":
        "gzip, deflate",
        "Accept-Language":
        "en-us"
    }
    #请求参数
    my_para = {"MallID": 10025, "Header": {"Token": token}}

    try:
        response = requests.post(url, json=my_para, headers=my_headers)
        log("签到结果：" + response.text)
    except Exception as e:
        raise e