"""
homes.jp 的工具类
"""
import hashlib
import math
import random
import time

from homesjpspider.utils.hash_util import Hash_Util


class Homesjp_Util():
    '''
    @msg: 生成时间戳 毫秒级
    @param {type} 
    @return: 
    '''
    @staticmethod
    def __getTimeStamp():
        return int(time.time() * 1000)
    @staticmethod
    def __t(e):
        t = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        n = ""
        r = 0
        while e > r:
            r += 1
            index = math.floor(random.random() * len(t))
            n += t[index:index + 1]
        return n
    '''
    @msg: 生成homesjp所需的proof参数
    @return: 
    '''
    @classmethod
    def genProof(cls):
        para2 = cls.__getTimeStamp()
        para3 = cls.__t(20)
        e = str(para2) + ":" + para3
        a = math.pow(2, 32 - 8)
        i = 0
        while True:
            o = hex(i)[2:] + ":" + e
            i += 1
            s = Hash_Util.sha1(o)
            if int(s[0:8], 16) < a:
                print("Proof is [{0}]".format(o))
                return o
