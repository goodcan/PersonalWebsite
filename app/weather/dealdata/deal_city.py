#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

TEMPEROTURE = {
    'data': []
}

DATA = []

with open('../data/data.json', 'r') as fr:
    spider_city = json.load(fr)

for value in spider_city.values():
    for city, t in value.items():
        city_t = {}
        city_t['name'] = city
        city_t['value'] = t
        TEMPEROTURE['data'].append(city_t)

        # print 'name:' + city + ' ' + 'value:' + t

# with open('../data/city_temperoture.json', 'w') as fw:
#     fw.write(json.dumps(TEMPEROTURE, ensure_ascii=False).encode('utf-8'))
#
# with open('../data/city_temperoture.json', 'r') as fr:
#     city_t = json.load(fr)

city_t_l = TEMPEROTURE['data']


with open('../data/geocoding.json', 'r') as fr:
    city_c = json.load(fr)

city_c_d = city_c['geoCoord']

count = 0
for each in city_t_l:
    try:
        DATA_DICT = {}
        DATA_DICT['name'] = each['name'].encode('utf-8')
        DATA_DICT['value'] = city_c_d[each['name']]
        DATA_DICT['value'].append(each['value'])
        # print DATA_DICT
        DATA.append(DATA_DICT)
    except Exception as e:
        count += 1

# print count
# print DATA

with open('../data/mydata.json', 'w') as fw:
    fw.write(json.dumps(DATA, ensure_ascii=False).encode('utf-8'))