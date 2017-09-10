#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, ValidationError
from wtforms.validators import Length, Required, DataRequired, EqualTo, Email
from ..models import User

class LoginForm(Form):
    username = StringField(validators=[
        DataRequired(message=u'用户名不能为空'),
        Length(2, 12, message=u'请输入6-12长度的字符')])
    password = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        Length(6, 12, message=u'请输入6-12长度的字符')])
    remember_me = BooleanField(u'保持登入')


class RegisterForm(Form):
    username = StringField(validators=[
        DataRequired(message=u'用户名不能为空'),
        Length(2, 12, message=u'请输入6-12长度的字符')])
    telephone = StringField(validators=[
        DataRequired(message=u'手机号码不能为空'),
        Length(11, 11, message=u'手机号码格式不对')])
    email = StringField(validators=[
        DataRequired(message=u'电子邮箱不能为空'),
        Length(1, 64, message=u'电子邮箱格式不对'),
        Email(message=u'电子邮箱格式不对')])
    password1 = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        Length(6, 12, message=u'请输入6-12长度的字符'),
        EqualTo('password2', message=u'密码不一致')])
    password2 = PasswordField(validators=[
        DataRequired(message=u'密码不能为空'),
        Length(6, 12, message=u'请输入6-12长度的字符')])

    # def validate_username(self, filed):
    #     if User.query.filter_by(username=filed.data).first():
    #         raise ValidationError(u'该用户名已经注册')
    #
    # def validate_telephone(self, filed):
    #     if User.query.filter_by(telephone=filed.data).first():
    #         raise ValidationError(u'该手机号码已经注册')
    #
    # def validate_email(self, filed):
    #     if User.query.filter_by(email=filed.data).first():
    #         raise ValidationError(u'该子邮箱已经注册')