#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class User(UserMixin, db.Model):
    """
    默认属性和方法：
    is_authenticated:当用户通过验证时,也即提供有效证明时返回True,（只有通过验证的用户会满足login_required的条件）
    is_active:如果这是一个活动用户且通过验证,账户也已激活,未被停用,也不符合任何你的应用拒绝一个账号的条件,返回True.
              不活动的账号可能不会登入（当然,是在没被强制的情况下）。
    is_anonymous:如果是一个匿名用户,返回True.（真实用户应返回False）
    get_id():返回一个能唯一识别用户的,并能用于从user_loader回调中加载用户的unicode.
             注意必须是一个unicode,如果ID原本是一个int或其它类型,你需要把它转换为unicode
    """
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    telephone = db.Column(db.String(11), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    confirmed = db.Column(db.Boolean, default=False)

    # 给User类添加属性
    @property
    def password(self):
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成一个带时间限制的JSON WEB签名
    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    # 验证令牌
    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        else:
            self.confirmed = True
            return True

    # 生成重置密码的令牌
    def generate_resetpwd_token(self, new_password, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset': self.id,
                        'new_password': new_password})

    def reset_password(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data['reset'] != self.id:
            return False
        else:
            self.password = data['new_password']
            return True

    def __repr__(self):
        return '[user: {}]'.format(self.username.encode('gb18030'))


# 加载用户的回调函数,接收以Unicode字符串形式的用户标识
@login_manager.user_loader
def load_user(user_id):
    print 'current_user: ' + user_id
    user = User.query.get(int(user_id))
    return user


class Permission:
    """权限常量"""
    FOLLOW = 0x01
    COMMENT = 0x02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')
