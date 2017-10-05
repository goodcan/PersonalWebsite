#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user
from . import starwar

@starwar.route('/index/')
def index():
    context = {}
    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None
    return render_template('starwar/starwar.html', **context)
