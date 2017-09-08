#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, flash, redirect, abort, render_template, url_for
from flask_login import login_user, logout_user, login_required
from . import auth
from .. import login_manager
from ..models import User
from forms import LoginForm
import json


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

        user_data = data['data']
        username = user_data['username']
        password = user_data['password']
        form = LoginForm(username=username, password=password)
        if form.validate():
            user = User.query.filter_by(username=username).first()
            if user:
                if user.password == password:
                    re = {'status': True,
                          'data': {
                              'username': username
                          }}
                    return jsonify(re)
                else:
                    re = {'status': False,
                          'data': {
                              'username': 1,
                              'password': 3
                          }}
                    return jsonify(re)
            else:
                re = {'status': False,
                      'data': {
                          'username': 2
                      }}
                return jsonify(re)
        else:
            re = {'status': False, 'data': {}}
            for key, value in form.errors.items():
                print key + ':' + value[0]
                re['data'][key] = value[0]
            return jsonify(re)
    return render_template('login.html')
