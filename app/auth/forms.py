#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import length, Required, DataRequired, EqualTo


class LoginForm(Form):
    username = StringField('username',validators=[
        DataRequired(message=u'数据不能为空'),
        length(6, 11, message=u'字符长度不对')])
    password = PasswordField(u'密码:', validators=[
        DataRequired(message=u'数据不能为空'),
        length(6, 11, message=u'字符长度不对')])
    # password2 = PasswordField(u'密码:')
    # remember_me = BooleanField('remember_me')