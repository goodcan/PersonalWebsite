#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import request, flash, redirect, abort, render_template, url_for
from flask_login import login_user, logout_user ,login_required
from . import auth
from .. import login_manager
from ..models import User

#加载用户，传入的数据必须是Unicode
@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    # elif request.method == 'POST':
    #
    #
    #     #验证用户并登入
    #     if form.validate_on_submit():
    #
    #
    #         login_user(user)
    #
    #         flash('Logged in successfully.')
    #
    #         #获取跳转前的页面位置
    #         next = request.args.get('next')
    #
    #         #验证跳转前的页面是否存在
    #         # if not next_is_valid(next):
    #         #     return abort(400)
    #
    #         return redirect(next or url_for('main.index'))


# @auth.route("/logout")
# @login_required
# def logout():
#     logout_user()
