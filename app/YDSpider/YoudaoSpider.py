#!/usr/bin/python
# -*- coding: utf-8 -*-

from time import time
from random import randint
from hashlib import md5
import requests, json

import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class MyTranslation(object):
    def __init__(self, question):
        self.question = question
        self.headers = {
            'Host': 'fanyi.youdao.com',
            'Origin': 'http://fanyi.youdao.com',
            'Pragma': 'no-cache',
            'Referer': 'http://fanyi.youdao.com/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 \
               (KHTML, like Gecko) Chrome/61.0.3153.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }

    def GetData(self):
        """
        分析有道翻译的fanyi.js，破解其中salt和sign参数的生成方式
        通过python模拟生成salt和sign的参数
        """
        timestamp = str(int(time() * 1000) + randint(0, 10))

        u = "fanyideskweb"
        d = self.question
        f = timestamp
        c = "rY0D^0'nM0}g5Mm1z%1G4"
        sign = md5((u + d + f + c).encode('utf-8')).hexdigest()

        data = {
            'i': self.question,
            'from': 'AUTO',
            'to': 'AUTO',
            'smartresult': 'dict',
            'client': 'fanyideskweb',
            'salt': timestamp,
            'sign': sign,
            'doctype': 'json',
            'version': '2.1',
            'keyfrom': 'fanyi.web',
            'action': 'FY_BY_CLICKBUTTION',
            'typoResult': 'true'
        }

        return data

    def GetAns(self):
        url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule&sessionFrom='
        req = requests.post(url=url, headers=self.headers, data=self.GetData())
        ans = json.loads(req.content, encoding='utf-8')

        return ans['translateResult'][0][0]['tgt']


if __name__ == '__main__':
    while 1:
        question = raw_input('输入需要翻译的内容:')
        test = MyTranslation(question).GetAns()
        print test
        if question == '.':
            break
