#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, g
from flask_login import login_required
from . import main
from .. import csrf
import json

# @csrf.exempt
@main.route('/index/')
@login_required
def index():
    print g.user
    data = g.user
    return render_template('index.html', data=data)
