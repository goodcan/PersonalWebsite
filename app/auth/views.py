#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, flash, redirect, abort, render_template, url_for
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import login_manager
from ..models import User
from forms import LoginForm
import json

#加载用户，传入的数据必须是Unicode
@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user

class ValidateLogin(object):
    def __init__(self):
        self.data = json.loads(request.get_data(), encoding='utf-8')

    def validate_on_submit(self):
        user_data = self.data['data']

        print '*' * 40
        print user_data['username']
        print '*' * 40
        form = LoginForm(remeber_me=user_data['username'])
        print form.validate()

        user = User.query.filter_by(username=user_data['username']).first()

        if user:
            print self.data
        else:
            print 'error'

@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        # data = request.get_json()

        # vaildata_data = ValidateLogin()
        # vaildata_data.validate_on_submit()
        data = json.loads(request.get_data(), encoding='utf-8')
        user_data = data['data']
        print type(user_data['username'])
        print user_data['username'], user_data['password']
        form = LoginForm(password=user_data['username'],password2=user_data['password'])
        print form.validate()

        re = {'response': True}

        return jsonify(re)
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
