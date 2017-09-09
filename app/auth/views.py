#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, flash, redirect, abort, render_template, url_for
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import login_manager
from ..models import User
from forms import LoginForm, RegisterForm
import json
from .. import csrf, db


# 加载用户，传入的数据必须是Unicode
@login_manager.user_loader
def load_user(user_id):
    user = User()
    return user


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    if request.method == 'POST':
        data = json.loads(request.get_data(), encoding='utf-8')

        print data
        user_data = data['data']
        username = user_data['username']
        password = user_data['password']
        login_form = LoginForm(username=username, password=password)
        if login_form.validate():
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    re = {'status': True,
                          'data': {
                              'username': username
                          }}
                    print user
                    return jsonify(re)
                else:
                    re = {'status': False,
                          'data': {
                              'username': [0, u'账号正确'],
                              'password': [2, u'密码错误']
                          }}
                    return jsonify(re)
            else:
                re = {'status': False,
                      'data': {
                          'username': [2, u'账号不存在']
                      }}
                return jsonify(re)
        else:
            re = {'status': False, 'data': {}}
            for key, value in login_form.errors.items():
                print key + ':' + value[0]
                re['data'][key] = [1, value[0]]
            return jsonify(re)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        data = json.loads(request.get_data(), encoding='utf-8')

        print data

        register_data = data['data']
        username = register_data['username']
        telephone = register_data['telephone']
        password1 = register_data['password1']
        password2 = register_data['password2']

        register_form = RegisterForm(username=username,
                                     telephone=telephone,
                                     password1=password1,
                                     password2=password2)
        if register_form.validate():
            user_name = User.query.filter_by(username=username).first()
            user_tel = User.query.filter_by(telephone=telephone).first()

            re = {'status': True, 'data': {
                'password1': [0, u'密码设置正确'],
                'password2': [0, u'']
            }}
            if user_name:
                re['status'] = False
                re['data']['username'] = [2, u'该用户名已经注册']
            else:
                re['data']['username'] = [0, u'用户名设置正确']
            if user_tel:
                re['status'] = False
                re['data']['telephone'] = [2, u'该用手机号码已经注册']
            else:
                re['data']['telephone'] = [0, u'手机号码设置正确']

            if re['status']:
                user = User(
                    username=username,
                    telephone=telephone,
                    password=password1
                )
                db.session.add(user)
                db.session.commit()
                return jsonify(re)
            else:
                return jsonify(re)
        else:
            re = {'status': False, 'data': {}}
            for key, value in register_form.errors.items():
                print key + ':' + value[0]
                re['data'][key] = [2, value[0]]
            return jsonify(re)
