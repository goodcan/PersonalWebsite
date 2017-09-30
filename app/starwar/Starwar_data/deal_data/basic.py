# -*- coding: utf-8 -*-

import json

f = open('../csv/films.txt', 'r')

fb = open('../csv/basic.csv', 'w')
fb.write('title,key,value\n')

for line in f:
    tmp = json.loads(line.strip('\n'))
    fb.write(tmp['title'] + ',' + 'characters,' + str(len(tmp['characters'])) + '\n')
    fb.write(tmp['title'] + ',' + 'planets,' + str(len(tmp['planets'])) + '\n')
    fb.write(tmp['title'] + ',' + 'starships,' + str(len(tmp['starships'])) + '\n')
    fb.write(tmp['title'] + ',' + 'vehicles,' + str(len(tmp['vehicles'])) + '\n')
    fb.write(tmp['title'] + ',' + 'species,' + str(len(tmp['species'])) + '\n')

f.close()
fb.close()