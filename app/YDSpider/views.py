#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request, jsonify
from YoudaoSpider import MyTranslation
from . import trans
from ..common import check_login
from json import loads

@trans.route('/youdao_spider/', methods=['GET', 'POST'])
def youdao_spider():
    if request.method == 'GET':
        context = {
            'user': check_login()
        }

        return render_template('YDSpider/index.html', **context)

    if request.method == 'POST':
        re = {'status': True, 'data': {}}
        data = loads(request.get_data(), encoding='utf-8')

        question = data['data']['question']
        print 'question:' + question
        if question == '':
            re['status'] = False
            re['data']['message-title'] = u'输入有误'
            re['data']['message-content'] = u'需要翻译的内容不能为空哦！'

            return jsonify(re)
        else:
            re['data']['answer'] = MyTranslation(question).GetAns()
            print 'answer:' + re['data']['answer']
            return jsonify(re)
