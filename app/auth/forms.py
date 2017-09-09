#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import length, Required, DataRequired, EqualTo


class LoginForm(Form):
    username = StringField(validators=[
        DataRequired(message=u'用户名不能为空'),
        length(6, 11, message=u'请输入6-11长度的字符')])
    password = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        length(6, 12, message=u'请输入6-11长度的字符')])


class RegisterForm(Form):
    username = StringField(validators=[
        DataRequired(message=u'用户名不能为空'),
        length(6, 11, message=u'请输入6-11长度的字符')])
    telephone = StringField(validators=[
        DataRequired(message=u'手机号码不能为空'),
        length(11, 11, message=u'手机号码格式不对')
    ])
    password1 = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        length(6, 12, message=u'请输入6-11长度的字符'),
        EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        length(6, 12, message=u'请输入6-11长度的字符')])
