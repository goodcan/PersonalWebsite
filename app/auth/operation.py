#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, redirect, render_template, url_for, g, flash
from flask_login import login_user, logout_user, login_required, current_user
from forms import ResetEmailForm, UsernameLoginForm, TelephoneLoginForm, RegisterForm, ResetPasswordForm
from datetime import datetime
from . import auth
from .. import db
from ..models import User
from ..email import send_email
from ..common import response_messages
from json import loads


@auth.before_app_request
def before_request():
    try:
        endpoint = request.endpoint
        endpoint_title = endpoint[:5]
    except:
        endpoint_title = None

    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed \
                and endpoint_title != 'auth.' \
                and endpoint != 'static':
            # print current_user.is_authenticated
            # print request.endpoint
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        title = 'login'
        return render_template('auth/register&login.html', title=title)

    if request.method == 'POST':
        data = loads(request.get_data(), encoding='utf-8')

        print data

        user_data = data['data']
        username = user_data['username']
        password = user_data['password']

        # 检测用户是以什么方式登入
        try:
            telephone = int(username)
            print telephone
            form = TelephoneLoginForm(telephone=username, password=password)
            g.user = User.query.filter_by(telephone=username).first()
        except:
            form = UsernameLoginForm(username=username, password=password)
            g.user = User.query.filter_by(username=username).first()
        g.re = {'status': True, 'data': {}}
        if form.validate():
            g.re['data']['confirmed'] = g.user.confirmed
            print g.user

            # 获取用户前一个请求地址
            next = request.args.get('next')
            if next:
                url_list = next.split('/')
                try:
                    if url_list[2] == 'user_profile':
                        url_list[3] = username
                        next = '/'.join(url_list)
                except:
                    print next

                print next

                g.re['data']['redirect'] = next
            else:
                print "next page is none"
                g.re['data']['redirect'] = url_for('main.index')
            remember_me = user_data['remember_me']
            g.user.ping()
            login_user(g.user, remember=remember_me)
            return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in form.errors.items():
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

        data = loads(request.get_data(), encoding='utf-8')

        print data

        register_data = data['data']
        username = register_data['username']
        telephone = register_data['telephone']
        email = register_data['email']
        password1 = register_data['password1']
        password2 = register_data['password2']

        form = RegisterForm(username=username,
                            telephone=telephone,
                            email=email,
                            password1=password1,
                            password2=password2)
        if form.validate():
            if g.re['status']:
                user = User(
                    username=username,
                    telephone=telephone,
                    email=email,
                    password=password1,
                    member_since=datetime.now()
                )
                db.session.add(user)
                db.session.commit()
                token = user.generate_confirmation_token()
                send_email(user.email, u'请验证你的账户', 'auth/email/confirm',
                           user=user, token=token)
                title = u'邮箱验证！'
                content = u'请查收验证邮件并及时完成验证！'
                response_messages(g.re, title, content)
                return jsonify(g.re)
            else:
                return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in form.errors.items():
                print key + ':' + str(value[0])
                re['data'][key] = value[0]
            return jsonify(re)


@auth.route("/logout/")
@login_required
def logout():
    """登出当前用户"""
    logout_user()
    re = {'status': True}
    return jsonify(re)


@auth.route('/confirm/<token>/<user_id>/')
# @login_required
def confirm(token, user_id):
    user = User.query.filter_by(id=user_id).first()
    if user:
        if user.confirmed:
            return redirect(url_for('main.index'))
        if user.confirm(token):
            print 'confirm success'
            message_title = u'邮箱验证成功'
            return render_template('auth/email/confirm_success.html', message_title=message_title)
        else:
            print 'confirm error'
            return redirect(url_for('auth.unconfirmed'))
    else:
        print 'confirm error'
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed/')
def unconfirmed():
    """
    返回验证失败的页面
    """
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('main.index'))
    logout_user()
    return render_template('auth/email/unconfirmed.html')


@auth.route('/resend_confirmation/')
@login_required
def resend_confirmation():
    """
    重新发送账户验证邮件
    """
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, u'请验证你的账户', 'auth/email/confirm',
               token=token, user=current_user)
    logout_user()
    re = {'message': u'请查收验证邮件并及时完成验证！'}
    return jsonify(re)


@auth.route('/reset_password_request/', methods=['GET', 'POST'])
def reset_password_request():
    """
    验证输入并发送修改密码的邮箱验证
    """
    # if not current_user.is_anonymous:
    #     print current_user.is_anonymous
    #     return redirect(url_for('main.index'))
    if request.method == 'GET':
        return render_template('auth/reset_password.html')
    if request.method == 'POST':
        g.re = {'status': True, 'data': {}}

        data = loads(request.get_data(), encoding='utf-8')

        print data

        resetpwd_data = data['data']
        email = resetpwd_data['email']
        password1 = resetpwd_data['passwordRS1']
        password2 = resetpwd_data['passwordRS2']

        form = ResetPasswordForm(email=email,
                                 password1=password1,
                                 password2=password2)
        if form.validate():
            if g.re['status']:
                user = User.query.filter_by(email=email).first()
                token = user.generate_resetpwd_token(password1)
                send_email(user.email, u'请验证您的账户并完成密码修改', 'auth/email/resetpwd_confirm',
                           user=user, token=token)
                title = u'邮箱验证'
                content = u'请查收验证邮件并及时完成验证！'
                response_messages(g.re, title, content)
                return jsonify(g.re)
            else:
                return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in form.errors.items():
                print key + ':' + str(value[0])
                re['data'][key] = value[0]
            return jsonify(re)


@auth.route('/reset_password/<token>/<user_id>/')
def reset_password(token, user_id):
    """
    邮箱验证并完成密码修改
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        if user.reset_password(token):
            print 'confirm success'
            message_title = u'密码修改成功'
            return render_template('auth/email/confirm_success.html', message_title=message_title)
        else:
            print 'confirm error'
            return redirect(url_for('auth.unconfirmed'))
    else:
        print 'confirm error'
        return redirect(url_for('auth.unconfirmed'))

@auth.route('/reset_email_request/', methods=['POST'])
@login_required
def reset_email_request():
    """
    验证输入并发送修改邮箱的邮箱验证
    """
    # if not current_user.is_anonymous:
    #     print current_user.is_anonymous
    #     return redirect(url_for('main.index'))

    if request.method == 'POST':
        g.re = {'status': True, 'data': {}}

        data = loads(request.get_data(), encoding='utf-8')

        print data

        resetemail_data = data['data']
        oldEmail = resetemail_data['oldEmailRS']
        newEmail = resetemail_data['newEmailRS']

        form = ResetEmailForm(oldEmail=oldEmail,
                              newEmail=newEmail)
        if form.validate():
            if g.re['status']:
                user = User.query.filter_by(email=oldEmail).first()
                token = user.generate_resetemail_token(newEmail)
                send_email(newEmail, u'请验证您的新邮箱', 'auth/email/resetemail_confirm',
                           user=user, token=token)
                title = u'邮箱验证'
                content = u'请查收验证邮件并及时完成验证！'
                response_messages(g.re, title, content)
                return jsonify(g.re)
            else:
                return jsonify(g.re)
        else:
            re = g.re
            re['status'] = False
            for key, value in form.errors.items():
                print key + ':' + str(value[0])
                re['data'][key] = value[0]
            return jsonify(re)

@auth.route('/reset_email/<token>/<user_id>/')
def reset_email(token, user_id):
    """
    邮箱验证并完成邮箱修改
    """
    user = User.query.filter_by(id=user_id).first()
    if user:
        if user.reset_email(token):
            print 'confirm success'
            message_title = u'邮箱修改成功'
            return render_template('auth/email/confirm_success.html', message_title=message_title)
        else:
            print 'confirm error'
            return redirect(url_for('auth.unconfirmed'))
    else:
        print 'confirm error'
        return redirect(url_for('auth.unconfirmed'))


@auth.route('/set_information/', methods=['POST'])
@login_required
def set_information():
    """
    设置用户个人信息
    """
    g.re = {'status': True, 'data': {}}

    user = current_user
    data = loads(request.get_data(), encoding='utf-8')

    set_information_data = data['data']
    name = set_information_data['name']
    location = set_information_data['location']
    about_me = set_information_data['about_me']

    if name == '':
        name = None
    if location == '':
        location = None
    if about_me == '':
        about_me = None

    user.name = name
    user.location = location
    user.about_me = about_me

    db.session.add(user)
    db.session.commit()

    title = u'消息'
    content = u'个人信息设置成功！'

    response_messages(g.re, title, content)

    return jsonify(g.re)
