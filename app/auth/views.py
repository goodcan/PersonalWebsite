#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, redirect, abort, render_template, url_for, g
from flask_login import login_user, logout_user, login_required
from forms import LoginForm, RegisterForm
from . import auth
from .. import login_manager, db, csrf
from ..models import User
import json


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        title = 'login'
        return render_template('auth/register&login.html', title=title)

    if request.method == 'POST':
        data = json.loads(request.get_data(), encoding='utf-8')

        print data

        user_data = data['data']
        username = user_data['username']
        password = user_data['password']
        login_form = LoginForm(username=username, password=password)
        g.re = {'status': True, 'data': {}}
        g.user = User.query.filter_by(username=username).first()
        if login_form.validate():
            print g.user
            next = request.args.get('next')
            if next:
                print next
                g.re['data']['redirect'] = next
            else:
                print "goto index"
                g.re['data']['redirect'] = url_for('main.index')
            remember_me = user_data['remember_me']
            login_user(g.user, remember=remember_me)
            return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in login_form.errors.items():
                print key + ':' + str(value[0])
                re['data'][key] = value[0]
            return jsonify(re)


@auth.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        title = 'register'
        return render_template('auth/register&login.html', title=title)

    if request.method == 'POST':
        g.re = {'status': True, 'data': {}}

        data = json.loads(request.get_data(), encoding='utf-8')

        print data

        register_data = data['data']
        username = register_data['username']
        telephone = register_data['telephone']
        email = register_data['email']
        password1 = register_data['password1']
        password2 = register_data['password2']

        register_form = RegisterForm(username=username,
                                     telephone=telephone,
                                     email=email,
                                     password1=password1,
                                     password2=password2)
        if register_form.validate():
            if g.re['status']:
                user = User(
                    username=username,
                    telephone=telephone,
                    email=email,
                    password=password1
                )
                db.session.add(user)
                db.session.commit()
                return jsonify(g.re)
            else:
                return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in register_form.errors.items():
                print key + ':' + str(value[0])
                re['data'][key] = value[0]
            return jsonify(re)

@auth.route("/logout/")
@login_required
def logout():
    logout_user()
    re = {'status': True}
    return jsonify(re)