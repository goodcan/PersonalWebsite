#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import current_user
from . import main
from ..common import check_login

# @csrf.exempt
@main.route('/')
# @login_required
def index():
    context = {
        'user': check_login(),
        'carousel_imgs': ['1', '2', '3']
    }

    return render_template('index.html', **context)
