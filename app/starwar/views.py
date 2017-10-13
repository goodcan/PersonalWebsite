#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user
from . import starwar
from ..common import check_login

@starwar.route('/index/')
def index():
    context = {
        'user': check_login()
    }

    return render_template('starwar/index.html', **context)
