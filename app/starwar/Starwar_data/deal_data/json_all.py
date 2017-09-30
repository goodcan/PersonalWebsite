#!/usr/bin/python
# -*- coding: utf-8 -*-

import json

data = {}

with open('../csv/films.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['title']] = tmp
with open('../csv/characters.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['name']] = tmp
with open('../csv/planets.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['name']] = tmp
with open('../csv/starships.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['name']] = tmp
with open('../csv/vehicles.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['name']] = tmp
with open('../csv/species.txt', 'r') as fr:
    for line in fr:
        tmp = json.loads(line.strip('\n'))
        data[tmp['name']] = tmp

with open('../templates/all.json', 'w') as fw:
    fw.write(json.dumps(data))

