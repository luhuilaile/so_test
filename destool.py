import datetime
import codecs
import requests
import os
import json
import time
import random
from pyquery import PyQuery as pq
import ctypes
so = ctypes.CDLL('./libDesTool.so')
''' public static native byte[] decrypt(byte[] bArr, byte[] bArr2, int i);
    public static native String signToken(String str, String str2, String str3, String str4);
'''
def so_signToken(str1,  str2,  str3,  str4):
    return so.signToken( str1,  str2,  str3,  str4)
def so_decrypt(bArr,bArr2, i):
    return so. decrypt( bArr,bArr2, i)
test_dict = {
    "platform": "Android",
    "type_value": "600",
    "device_id": "580c2adea07af6c1",
    # "antifraud_ts": "1600155399",
    # "antifraud_tid": "5025506806",
    # "antifraud_sign": "079n6n310r88p958347nr5pn397s5q9pr61p6701",
    "client_v": "1.380",
    "type": "times"
}
temp = []


# 请求参数拼接
def str_append(map, j, stri):
    hashMap = {}
    for str2 in sorted(map):
        if not str2 == "uid" or str2 == "antifraud_tid" or str == "antifraud_sign" or str2 == "antifraud_ts":
            hashMap[str2] = map[str2]
    builder = []
    obj = 1
    for key in sorted(hashMap):
        if obj is None:
            builder.append("|")
        if not hashMap[key] is None and not hashMap[key] == "":
            builder.append(hashMap[key])
        obj = None
    stringBuilder2 = "".join(builder)
    stringBuilder = []
    stringBuilder.append("paramValues:")
    stringBuilder.append(stringBuilder2)
    print("".join(stringBuilder))
    stringBuilder3 = []
    stringBuilder3.append(" currentUnixTime=")
    stringBuilder3.append(j)
    stringBuilder3.append(" paramValues=")
    stringBuilder3.append(stringBuilder2)
    stringBuilder3.append(" token=")
    stringBuilder3.append(stri)
    print("errorToken" + "".join(stringBuilder3))
    stringBuilder = []
    stringBuilder.append(str(j))
    stringBuilder.append("")
    str3 = so_signToken("".join(stringBuilder), stringBuilder2, stri, "shuabu")
    return str3


# 对参数进行解密
def decrypt_data(stri, str2):
    import base64
    decode = base64.b64decode(stri).decode("utf-8")
    #decode.encode() 字符串转字节数组
    decod = so_decrypt(decode.encode(), str2.getBytes(), 0)
    # 字节数组转字符串
    return decod.decode()


def get_token():
    token = "MGYxZWO0zYEcHrJatWZMRxAIpSmnZDNlMDIwYjdiZTh2OnYxLjM="
    anti_device_id = "beeeb3c3c48b8efa6ae6ae10663cfef9"
    r = decrypt_data(token, anti_device_id)
    return r


def wrap_des(hashMap):
    currentTimeMillis = 1600155399
    a = str_append(hashMap, currentTimeMillis, get_token())
    temp.append("_sign=")
    temp.append(a)
    hashMap["antifraud_sign"] = a
    hashMap["antifraud_ts"] = '{time}'.format(time=currentTimeMillis)
    hashMap["antifraud_tid"] = "5025506806"
    return str(hashMap)


def job():
    result = wrap_des(test_dict)
    print(result)


if __name__ == '__main__':
    job()
