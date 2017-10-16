#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import sleep
import requests
import urllib
import hashlib
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def get_url(address):
    atoken = '6f55WyqsOb7viBsuT8oF5XFGYI5Acsha'
    stoken = 'IztM4COvEFVGSd0Z1mugtout6tWs8HPW'

    # 以get请求为例http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak
    queryStr = '/geocoder/v2/?address=' + address + '&output=json&ak=' + atoken

    # 对queryStr进行转码，safe内的保留字符不转换
    encodedStr = urllib.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")

    # 在最后直接追加上yoursk
    rawStr = encodedStr + stoken

    # md5计算出的sn值7de5a22212ffaa9e326444c75a58f9a0
    # 最终合法请求url是http://api.map.baidu.com/geocoder/v2/?address=百度大厦&output=json&ak=yourak&sn=7de5a22212ffaa9e326444c75a58f9a0
    sn = hashlib.md5(urllib.quote_plus(rawStr)).hexdigest()

    url = 'http://api.map.baidu.com' + queryStr + '&sn=' + sn
    res = json.loads(requests.get(url).content)
    if res['status'] == 0:
        location = res['result']['location']
        geocoding = [location['lng'], location['lat']]
    else:
        geocoding = None

    return geocoding


with open('../data/data.json', 'r') as fr:
    citys = json.load(fr)

geoCoord = {}

for key, value in citys.items():
    print '*' * 40
    print key
    print '*' * 40
    for each in value:
        print each
        address = each.encode('utf-8')
        geoCoord.update({address: get_url(address)})
        sleep(0.5)

data = {'geoCoord': geoCoord}

with open('../data/geocoding.json', 'w') as fw:
    fw.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
