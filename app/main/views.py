#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, g
from flask_login import login_required, current_user
from . import main

# @csrf.exempt
@main.route('/index/')
@login_required
def index():
    data = {}
    data['username'] = current_user.username
    data['carousel_imgs'] = ['1', '2', '3']
    return render_template('index.html', data=data)
