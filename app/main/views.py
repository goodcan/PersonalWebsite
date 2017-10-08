#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user
from . import main

# @csrf.exempt
@main.route('/')
# @login_required
def index():
    context = {}
    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = None
    context['carousel_imgs'] = ['1', '2', '3']

    return render_template('index.html', **context)
