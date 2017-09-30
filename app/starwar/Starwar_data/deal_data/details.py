# -*- coding: utf-8 -*-

import urllib
import urllib2
import json


def GetData(url):
    request = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(request, timeout=2)
    result = response.read()
    return result

headers = {
    'User-Agent': 'ozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3153.0 Safari/537.36'
}

with open('../csv/films.txt', 'r') as f:
    films = []
    for line in f:
        line = json.loads(line.strip('\n'))
        films.append(line)

#目标：人物、星球、星舰、装备、种族
targets = ["characters", "planets" , "starships", "vehicles", "species"]

for target in targets:
    with open('csv/' + target + '.txt', 'w') as f:
        data = []
        for item in films:
            tmp = item[target]
            for t in tmp:
                if t in data:
                    continue
                else:
                    data.append(t)

                while True:
                    print t
                    try:
                        result = GetData(t)
                    except Exception, e:
                        continue
                    else:
                        f.write(result + '\n')
                        break

        print target, len(data)