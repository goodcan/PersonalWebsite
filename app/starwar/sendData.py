#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify
import json
from . import starwar

import os
basedir = os.path.abspath(os.path.dirname(__file__))

@starwar.route('/<fileJson>/')
def sendJson(fileJson):
    with open(basedir + '/Starwar_data/json/' + fileJson, 'r') as f:
        data = json.load(f)
    return jsonify(data)