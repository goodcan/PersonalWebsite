#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from time import sleep
import requests, json

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class ChinaWeatherData(object):
    def __init__(self):
        self.DISTRICT_LIST = ['hb', 'db', 'hd', 'hz', 'hn', 'xb', 'xn', 'gat']
        self.DATA_DICT = {}
        self.HEARDERS = {
            'Host': 'www.weather.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'http://www.weather.com.cn/textFC/db.shtml',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3153.0 Safari/537.36'
        }


    def GetData(self, each_url, headers):
        url = 'http://www.weather.com.cn/textFC/' + each_url + '.shtml'
        req = requests.get(url, headers=headers)
        content = req.content
        soup = BeautifulSoup(content, 'lxml')

        # find只查找第一个，find_all查找第全部

        if each_url == 'gat':

            all_table = soup.find('div', class_='conMidtab')
            table_list = all_table.find('div', class_="conMidtab2")

            tr_list = table_list.find_all('tr')[:11]

            td_list = tr_list[2].find_all('td')
            province = td_list[0].find('a').text
            city = td_list[1].find('a').text
            try:
                temperoture = int(td_list[4].text)
            except Exception as e:
                temperoture = int(td_list[7].text)
            self.DATA_DICT[province] = {}
            self.DATA_DICT[province][city] = temperoture

            td_list = tr_list[5].find_all('td')
            province = td_list[0].find('a').text
            city = td_list[1].find('a').text
            try:
                temperoture = int(td_list[4].text)
            except Exception as e:
                temperoture = int(td_list[7].text)
            self.DATA_DICT[province] = {}
            self.DATA_DICT[province][city] = temperoture

            tr_tw = tr_list[8:]
            for index, tr in enumerate(tr_tw):
                if index == 0:
                    td_list = tr.find_all('td')
                    province = td_list[0].find('a').text
                    city = td_list[1].find('a').text
                    try:
                        temperoture = int(td_list[4].text)
                    except Exception as e:
                        temperoture = int(td_list[7].text)
                    self.DATA_DICT[province] = {}
                    self.DATA_DICT[province][city] = temperoture
                else:
                    td_list = tr.find_all('td')
                    city = td_list[0].find('a').text
                    try:
                        temperoture = int(td_list[3].text)
                    except Exception as e:
                        temperoture = int(td_list[6].text)
                    self.DATA_DICT[province][city] = temperoture

        else:

            all_table = soup.find('div', class_='conMidtab')
            table_list = all_table.find_all('div', class_="conMidtab2")

            for each_table in table_list:
                tr_list = each_table.find_all('tr')[2:]

                for index, tr in enumerate(tr_list):

                    if index == 0:
                        td_list = tr.find_all('td')
                        province = td_list[0].find('a').text
                        city = td_list[1].find('a').text
                        try:
                            temperoture = int(td_list[4].text)
                        except Exception as e:
                            temperoture = int(td_list[7].text)
                        self.DATA_DICT[province] = {}
                        self.DATA_DICT[province][city] = temperoture

                    else:
                        td_list = tr.find_all('td')
                        city = td_list[0].find('a').text
                        try:
                            temperoture = int(td_list[3].text)
                        except Exception as e:
                            temperoture = int(td_list[6].text)
                        self.DATA_DICT[province][city] = temperoture

    def ReturnData(self):
        for each_url in self.DISTRICT_LIST:
            print '*' * 40
            print each_url
            print '*' * 40

            self.GetData(each_url, self.HEARDERS)
            sleep(1)

        return self.DATA_DICT
            # json.dumps 序列化时默认使用的ascii编码，想输出真正的中文需要指定ensure_ascii=False
            # with open('../data/data1.json', 'w') as fw:
            #     fw.write(json.dumps(self.DATA_DICT, ensure_ascii=False).encode('utf-8'))

# if __name__ == '__main__':
#     main(DISTRICT_LIST, self.HEARDERS)
# a = ChinaWeatherData()
# d = a.ReturnData()
# print d
