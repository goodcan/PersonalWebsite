#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import abort, render_template, url_for, request, redirect, g
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import User, Permission
from . import main

# @csrf.exempt
@main.route('/')
@login_required
def index():
    context = {
        'user':current_user,
        'carousel_imgs': ['1', '2', '3']
    }
    return render_template('index.html', **context)

@main.route('/user/<username>/')
@login_required
def user(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    context = {
        'user':user
    }
    if user is None:
        abort(404)
    return render_template('user.html', **context)