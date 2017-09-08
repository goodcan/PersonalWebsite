#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template
from flask_login import login_required
from . import main
from ..auth.forms import LoginForm

@main.route('/')
# @login_required
def index():
    form = LoginForm
    return render_template('index.html', form=form)