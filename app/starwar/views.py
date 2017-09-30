#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from . import starwar

@starwar.route('/index/')
def index():
    return render_template('starwar/starwar.html')
