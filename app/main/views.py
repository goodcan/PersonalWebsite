#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import abort, render_template, url_for, request, redirect, g
from flask_login import confirm_login, current_user
from ..decorators import admin_required, permission_required
from ..models import User, Permission
from . import main

# @csrf.exempt
@main.route('/')
# @login_required
def index():
    context = {}
    if current_user.is_authenticated:

        # 恢复新鲜，优化记住密码功能
        confirm_login()

        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None
    context['carousel_imgs'] = ['1', '2', '3']
    return render_template('index.html', **context)
