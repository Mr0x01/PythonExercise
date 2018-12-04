# -*- coding: utf-8 -*-
import scrapy
import urllib
import logging
from homesjpspider.utils.homesjp_util import Homesjp_Util
from homesjpspider.items import *
import json
import urllib


class Homesjpcookie(scrapy.Spider):
    name = "homesjpcookie"
    custom_settings = {
        "DOWNLOAD_DELAY":1
    }
    def start_requests(self):
        if Building.table_exists() == False:
            Building.create_table()
        if UnitModel.table_exists() == False:
            UnitModel.create_table()
        if CookieModel.table_exists() == False:
            CookieModel.create_table()
        # 转至list页，不跟随redirect，获取TS01ec9519
        return [
            scrapy.Request(
                url="https://www.homes.co.jp/chintai/tokyo/23ku/list/",
                method="GET",
                cookies={},
                headers={},
                meta={"dont_redirect": True,
                      "url": "https://www.homes.co.jp/chintai/tokyo/23ku/list/"},
                callback=self.step1_callback,
                dont_filter=True
            )
        ]

    def step1_callback(self, response):
        cookie_list = response.headers.getlist("Set-Cookie")
        TS01ec9519 = None
        for cookie in cookie_list:
            cookie_str = cookie.decode("UTF-8")
            if cookie_str.find("TS01ec9519") > -1:
                TS01ec9519 = cookie_str.replace("TS01ec9519=", "").replace(
                    "; Path=/", "")
                break
        if TS01ec9519 != None:
            logging.info("获取到Cookie[TS01ec9519]:{0}".format(TS01ec9519))
            return scrapy.Request(
                url="http://www.homes.co.jp/nxtgrpdstl.js",
                method="GET",
                cookies={
                    "TS01ec9519": TS01ec9519  # 带着cookie请求js
                },
                callback=self.step2_callback,
                meta={"TS01ec9519": TS01ec9519, "url": response.meta["url"]},
                dont_filter=True
            )

    def step2_callback(self, response):
        js_body = response.body.decode("UTF-8")
        pid_start_index = js_body.find("PID=") + 4
        pid_end_index = pid_start_index + 36
        pid = js_body[pid_start_index:pid_end_index]  # 获取PID
        logging.info("获取到PID:{0}".format(pid))
        finger_print_json = {
            "proof": "247:1542086734677:CTYf3bwj7mpQitgeVOhO",
            "fp2": {
                "userAgent":
                "Mozilla/5.0(WindowsNT10.0;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/70.0.3538.77Safari/537.36",
                "language":
                "zh-CN",
                "screen": {
                    "width": 1280,
                    "height": 1024,
                    "availHeight": 994,
                    "availWidth": 1280,
                    "pixelDepth": 24,
                    "innerWidth": 1234,
                    "innerHeight": 617,
                    "outerWidth": 1250,
                    "outerHeight": 736,
                    "devicePixelRatio": 1
                },
                "timezone":
                8,
                "indexedDb":
                True,
                "addBehavior":
                False,
                "openDatabase":
                True,
                "cpuClass":
                "unknown",
                "platform":
                "Win32",
                "doNotTrack":
                "1",
                "plugins":
                "ChromePDFPlugin::PortableDocumentFormat::application/x-google-chrome-pdf~pdf;ChromePDFViewer::::application/pdf~pdf;NativeClient::::application/x-nacl~,application/x-pnacl~",
                "canvas": {
                    "winding": "yes",
                    "towebp": True,
                    "blending": True,
                    "img": "7fce9217391b3b610b9e5d1cfb31591793479a46"
                },
                "webGL": {
                    "img":
                    "bd6549c125f67b18985a8c509803f4b883ff810c",
                    "extensions":
                    "ANGLE_instanced_arrays;EXT_blend_minmax;EXT_color_buffer_half_float;EXT_disjoint_timer_query;EXT_frag_depth;EXT_shader_texture_lod;EXT_texture_filter_anisotropic;WEBKIT_EXT_texture_filter_anisotropic;EXT_sRGB;OES_element_index_uint;OES_standard_derivatives;OES_texture_float;OES_texture_float_linear;OES_texture_half_float;OES_texture_half_float_linear;OES_vertex_array_object;WEBGL_color_buffer_float;WEBGL_compressed_texture_s3tc;WEBKIT_WEBGL_compressed_texture_s3tc;WEBGL_compressed_texture_s3tc_srgb;WEBGL_debug_renderer_info;WEBGL_debug_shaders;WEBGL_depth_texture;WEBKIT_WEBGL_depth_texture;WEBGL_draw_buffers;WEBGL_lose_context;WEBKIT_WEBGL_lose_context",
                    "aliasedlinewidthrange":
                    "[1,1]",
                    "aliasedpointsizerange":
                    "[1,1024]",
                    "alphabits":
                    8,
                    "antialiasing":
                    "yes",
                    "bluebits":
                    8,
                    "depthbits":
                    24,
                    "greenbits":
                    8,
                    "maxanisotropy":
                    16,
                    "maxcombinedtextureimageunits":
                    32,
                    "maxcubemaptexturesize":
                    16384,
                    "maxfragmentuniformvectors":
                    1024,
                    "maxrenderbuffersize":
                    16384,
                    "maxtextureimageunits":
                    16,
                    "maxtexturesize":
                    16384,
                    "maxvaryingvectors":
                    30,
                    "maxvertexattribs":
                    16,
                    "maxvertextextureimageunits":
                    16,
                    "maxvertexuniformvectors":
                    4096,
                    "maxviewportdims":
                    "[16384,16384]",
                    "redbits":
                    8,
                    "renderer":
                    "WebKitWebGL",
                    "shadinglanguageversion":
                    "WebGLGLSLES1.0(OpenGLESGLSLES1.0Chromium)",
                    "stencilbits":
                    0,
                    "vendor":
                    "WebKit",
                    "version":
                    "WebGL1.0(OpenGLES2.0Chromium)",
                    "vertexshaderhighfloatprecision":
                    23,
                    "vertexshaderhighfloatprecisionrangeMin":
                    127,
                    "vertexshaderhighfloatprecisionrangeMax":
                    127,
                    "vertexshadermediumfloatprecision":
                    23,
                    "vertexshadermediumfloatprecisionrangeMin":
                    127,
                    "vertexshadermediumfloatprecisionrangeMax":
                    127,
                    "vertexshaderlowfloatprecision":
                    23,
                    "vertexshaderlowfloatprecisionrangeMin":
                    127,
                    "vertexshaderlowfloatprecisionrangeMax":
                    127,
                    "fragmentshaderhighfloatprecision":
                    23,
                    "fragmentshaderhighfloatprecisionrangeMin":
                    127,
                    "fragmentshaderhighfloatprecisionrangeMax":
                    127,
                    "fragmentshadermediumfloatprecision":
                    23,
                    "fragmentshadermediumfloatprecisionrangeMin":
                    127,
                    "fragmentshadermediumfloatprecisionrangeMax":
                    127,
                    "fragmentshaderlowfloatprecision":
                    23,
                    "fragmentshaderlowfloatprecisionrangeMin":
                    127,
                    "fragmentshaderlowfloatprecisionrangeMax":
                    127,
                    "vertexshaderhighintprecision":
                    0,
                    "vertexshaderhighintprecisionrangeMin":
                    31,
                    "vertexshaderhighintprecisionrangeMax":
                    30,
                    "vertexshadermediumintprecision":
                    0,
                    "vertexshadermediumintprecisionrangeMin":
                    31,
                    "vertexshadermediumintprecisionrangeMax":
                    30,
                    "vertexshaderlowintprecision":
                    0,
                    "vertexshaderlowintprecisionrangeMin":
                    31,
                    "vertexshaderlowintprecisionrangeMax":
                    30,
                    "fragmentshaderhighintprecision":
                    0,
                    "fragmentshaderhighintprecisionrangeMin":
                    31,
                    "fragmentshaderhighintprecisionrangeMax":
                    30,
                    "fragmentshadermediumintprecision":
                    0,
                    "fragmentshadermediumintprecisionrangeMin":
                    31,
                    "fragmentshadermediumintprecisionrangeMax":
                    30,
                    "fragmentshaderlowintprecision":
                    0,
                    "fragmentshaderlowintprecisionrangeMin":
                    31,
                    "fragmentshaderlowintprecisionrangeMax":
                    30
                },
                "touch": {
                    "maxTouchPoints": 0,
                    "touchEvent": False,
                    "touchStart": False
                },
                "video": {
                    "ogg": "probably",
                    "h264": "probably",
                    "webm": "probably"
                },
                "audio": {
                    "ogg": "probably",
                    "mp3": "probably",
                    "wav": "probably",
                    "m4a": "maybe"
                },
                "vendor":
                "GoogleInc.",
                "product":
                "Gecko",
                "productSub":
                "20030107",
                "browser": {
                    "ie": False,
                    "chrome": True,
                    "webdriver": False
                },
                "window": {
                    "historyLength": 2,
                    "hardwareConcurrency": 4,
                    "iframe": False
                },
                "fonts":
                "Calibri;Century;Haettenschweiler;Marlett;Pristina;SimHei"
            },
            "cookies": 1,
            "setTimeout": 0,
            "setInterval": 0,
            "appName": "Netscape",
            "platform": "Win32",
            "syslang": "zh-CN",
            "userlang": "zh-CN",
            "cpu": "",
            "productSub": "20030107",
            "plugins": {
                "0": "ChromePDFPlugin",
                "1": "ChromePDFViewer",
                "2": "NativeClient"
            },
            "mimeTypes": {
                "0": "application/pdf",
                "1": "PortableDocumentFormatapplication/x-google-chrome-pdf",
                "2": "NativeClientExecutableapplication/x-nacl",
                "3": "PortableNativeClientExecutableapplication/x-pnacl"
            },
            "screen": {
                "width": 1280,
                "height": 1024,
                "colorDepth": 24
            },
            "fonts": {
                "0": "Calibri",
                "1": "Cambria",
                "2": "Times",
                "3": "Constantia",
                "4": "LucidaBright",
                "5": "Georgia",
                "6": "SegoeUI",
                "7": "Candara",
                "8": "TrebuchetMS",
                "9": "Verdana",
                "10": "Consolas",
                "11": "LucidaConsole",
                "12": "LucidaSansTypewriter",
                "13": "CourierNew",
                "14": "Courier"
            }
        }
        finger_print_json["proof"] = Homesjp_Util.genProof()
        finger_print_str = urllib.parse.urlencode(finger_print_json)
        logging.info("生成Proof:{0}".format(finger_print_json["proof"]))
        return scrapy.FormRequest(
            "http://www.homes.co.jp/nxtgrpdstl.js?PID={0}".format(pid),
            cookies={"TS01ec9519": response.meta["TS01ec9519"]},
            method="POST",
            formdata={"p": finger_print_str},
            callback=self.step3_callback,
            meta={"url": response.meta["url"]},
            dont_filter=True
        )

    def step3_callback(self, response):
        cookie_list = response.headers.getlist("Set-Cookie")
        _cookies = {}
        for index in range(0, len(cookie_list)):
            temp_cookie = cookie_list[index].decode("utf-8").split(";")[0]
            key = temp_cookie.split("=")[0]
            value = temp_cookie.split("=")[1]
            _cookies[key] = value
            logging.info("{0}:{1}".format(key, value))
        return scrapy.Request(
            url="http://www.homes.co.jp/distil_identify_cookie.html?httpReferrer=%2Fchintai%2Ftokyo%2F23ku%2Flist%2F&uid={0}"
            .format(_cookies["D_UID"]),
            method="GET",
            cookies=_cookies,
            callback=self.step4_callback,
            meta={
                "dont_redirect": True,
                "cookies": _cookies,
                "url": response.meta["url"]
            },
            dont_filter=True
        )

    def step4_callback(self, response):
        _cookies = response.meta["cookies"]
        cookie = CookieItem()
        cookie["D_HID"] = _cookies["D_HID"]
        cookie["D_IID"] = _cookies["D_IID"]
        try:
            cookie["D_SID"] = _cookies["D_SID"]
        except Exception as identifier:
            cookie["D_SID"] = "114.254.102.180:dZGUnGIuhCZRm5jz5KJOPw55MNJu8S2tZrfxE4IbSWA"
            logging.warning("获取SID失败")
        
        cookie["D_UID"] = _cookies["D_UID"]
        cookie["D_ZID"] = _cookies["D_ZID"]
        cookie["D_ZUID"] = _cookies["D_ZUID"]
        cookie["TS01ec9519"] = _cookies["TS01ec9519"]
        yield cookie
        yield scrapy.Request(
            url="https://www.homes.co.jp/chintai/tokyo/23ku/list/",
            method="GET",
            cookies={},
            headers={},
            meta={"dont_redirect": True,
                  "url": "https://www.homes.co.jp/chintai/tokyo/23ku/list/"},
            callback=self.step1_callback,
            dont_filter=True
        )
