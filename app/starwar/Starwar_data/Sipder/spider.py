# -*- coding: utf-8 -*-

import urllib
import urllib2
import json

films = []
for x in xrange(1, 8):
    films.append('http://swapi.co/api/films/' + str(x) + '/')

headers = {
    'User-Agent': 'ozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3153.0 Safari/537.36'
}

with open('../csv/films.txt', 'w') as f:
    for item in films:
        print item
        request = urllib2.Request(url = item, headers=headers)
        response = urllib2.urlopen(request, timeout=2)
        result = response.read()
        print result
        f.write(result + '\n')