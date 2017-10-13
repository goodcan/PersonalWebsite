#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, jsonify
from makeData import MakeData
import json, os
from . import weather
from ..common import check_login

@weather.route('/')
def index():
    context = {
        'user': check_login()
    }

    return render_template('weather/index.html', **context)

@weather.route('/data.json/')
def sendData():
    make_data = MakeData()
    data = make_data.ReturnData()

    # basedir = os.path.abspath(os.path.dirname(__file__))
    # with open(basedir + '/data/mydata.json', 'r') as fr:
    #     data = json.load(fr)

    return jsonify(data)