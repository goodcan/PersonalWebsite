#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from . import auth
from ..models import User

@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    context = {
        'user':user
    }
    if user is None:
        abort(404)
    return render_template('user_profile.html', **context)
