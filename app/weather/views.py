#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from makeData import MakeData
from flask_login import current_user
import json, os
from . import weather

@weather.route('/')
def index():
    context = {}
    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None
    return render_template('weather/index.html', **context)

@weather.route('/data.json/')
def sendData():
    make_data = MakeData()
    data = make_data.ReturnData()

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # with open(basedir + '/data/mydata.json', 'r') as fr:
    #     data = json.load(fr)

    return jsonify(data)