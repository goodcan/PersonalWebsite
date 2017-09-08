#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import length, Required, DataRequired, EqualTo


class LoginForm(Form):
    # username = StringField('username', validators=[Required(),length(6, 11)])
    password = PasswordField(u'密码:', validators=[EqualTo('password2')])
    password2 = PasswordField(u'密码:')
    # remember_me = BooleanField('remember_me')

# class ChangePassword(Form):
#     password = PasswordField('New Password', [EqualTo('confirm', message='Passwords must match')])
#     confirm  = PasswordField('Repeat Password')