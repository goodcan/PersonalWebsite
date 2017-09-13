#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, redirect, render_template, url_for, g, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import LoginForm, RegisterForm
from . import auth
from .. import login_manager, db, csrf
from ..models import User
from ..email import send_email
import json


@auth.before_app_request
def before_request():
    try:
        endpoint = request.endpoint
        endpoint_title = endpoint[:5]
    except:
        endpoint_title = None
    if current_user.is_authenticated \
            and not current_user.confirmed \
            and endpoint_title != 'auth.' \
            and endpoint != 'static':
        # print current_user.is_authenticated
        # print request.endpoint
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed/')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    return render_template('auth/email/unconfirmed.html')


@auth.route('/resend_confirmation/')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'请验证你的账户', 'auth/email/confirm',
               token=token,  user=current_user)
    logout_user()
    re = {'message': u'请查收验证邮件并及时完成验证！'}
    return jsonify(re)

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
        g.user = User.query.filter_by(username=username).first()
        g.re = {'status': True, 'data': {}}
        if login_form.validate():
            g.re['data']['confirmed'] = g.user.confirmed
            print g.user
            next = request.args.get('next')
            if next:
                print next
                g.re['data']['redirect'] = next
            else:
                print "next page is none"
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
                token = user.generate_confirmation_token()
                send_email(user.email, u'请验证你的账户', 'auth/email/confirm',
                           user=user, token=token)
                g.re['data']['confirm'] = u'请查收验证邮件并及时完成验证！'
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


@auth.route('/confirm/<token>/<user_id>/')
# @login_required
def confirm(token, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user.confirmed:
        return redirect(url_for('main.index'))
    if user.confirm(token):
        print 'confirm success'
        return render_template('auth/email/confirm_success.html')
    else:
        print 'confirm error'
        return redirect(url_for('auth.unconfirmed'))
