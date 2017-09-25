#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import abort, render_template, url_for, request, redirect, g
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import User, Permission
from . import main

# @csrf.exempt
@main.route('/')
# @login_required
def index():
    context = {}
    if current_user.is_anonymous:
        context['user'] = {}
        context['user']['username'] = None
        print '*' * 40
    else:
        context['user'] = current_user
    context['carousel_imgs'] = ['1', '2', '3']
    return render_template('index.html', **context)