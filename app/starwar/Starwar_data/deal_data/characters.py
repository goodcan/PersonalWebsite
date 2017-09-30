# -*- coding: utf-8 -*-

import sys

reload(sys)
sys.setdefaultencoding('utf-8')

import json

fr = open('../csv/characters.txt', 'r')
fw = open('../csv/stat_character.csv', 'w')
fw.write('name,height,mass,gender,homeworld\n')

for line in fr:
    tmp = json.loads(line.strip('\n'))
    if tmp['height'] == 'unknown':
        tmp['height'] = '-1'
    if tmp['mass'] == 'unknown':
        tmp['mass'] = '-1'
    if tmp['gender'] == 'none':
        tmp['gender'] = 'n/a'
    fw.write(tmp['name'] + ',' + tmp['height'] + ',' + tmp['mass'] + ',' + tmp['gender'].strip() + ',' + tmp[
        'homeworld'] + '\n')

fw.close()
fr.close()
