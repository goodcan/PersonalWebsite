#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import db, login_manager

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    # 给User类添加属性
    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


    def __repr__(self):
        return '[user: {}]'.format(self.username.encode('gb18030'))

# 加载用户的回调函数,接收以Unicode字符串形式的用户标识
@login_manager.user_loader
def load_user(user_id):
    print user_id
    user = User.query.get(int(user_id))
    return user