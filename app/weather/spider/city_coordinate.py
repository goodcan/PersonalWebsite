#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from re import search
import requests
import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

DOORDINATE = {
    'geoCoord': {}
}

url = 'http://www.360doc.com/content/14/1222/11/502486_434782427.shtml'

headers = {
    'Host': 'www.360doc.com',
    'Pragma': 'no-cache',
    'Referer': 'https://www.baidu.com/link?url=LBRBWOvKgye0sNQmrrEiF7pFgB7lE4iE8N6VwWHIQWDvfHuqwNvWrCAP_5mdc7JKw5nhW \
    ITK5IEqtVtyLQpBPVHTkfgZVQO5w0nCF8edopq&wd=&eqid=a0f3ea3c000248ad000000045997c588',
    'Upgrade-Insecure-Requests': 1,
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3153.0 Safari/537.36'
}

req = requests.get(url, headers)
soup = BeautifulSoup(req.content, 'lxml')

table = soup.find(id='artContent')

tr_list = table.find_all('tr')[1:]


for each_tr in tr_list:
    td_list = each_tr.find_all('td')

    city = td_list[1].text
    try:
        longitude = search(r'\d+\.\d*', td_list[3].text).group()
        latitude = search(r'\d+\.\d*', td_list[2].text).group()
    except Exception:
        longitude = '113.40'
        latitude = '34.46'

    DOORDINATE['geoCoord'][city] = []
    DOORDINATE['geoCoord'][city].append(longitude)
    DOORDINATE['geoCoord'][city].append(latitude)

    # print city + ':' + '[' + longitude + ',' + latitude +']'

with open('../data/city_coordinate.json', 'w') as fw:
    fw.write(json.dumps(DOORDINATE, ensure_ascii=False).encode('utf-8'))

