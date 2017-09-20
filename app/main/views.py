#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import abort, render_template, request, redirect, g
from flask_login import login_required, current_user
from ..decorators import admin_required, permission_required
from ..models import User, Permission
from . import main

# @csrf.exempt
@main.route('/')
@login_required
def index():
    data = {}
    data['username'] = current_user.username
    data['carousel_imgs'] = ['1', '2', '3']
    return render_template('index.html', data=data)

@main.route('/user/<username>/')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    render_template('user.html', user=user)