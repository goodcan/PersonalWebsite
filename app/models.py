#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, current_app, request
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from . import db, login_manager
from datetime import datetime
from hashlib import md5
from threading import Thread
import sys, os, requests

reload(sys)
sys.setdefaultencoding('utf-8')

BASE_PWD = os.path.abspath(os.path.dirname('__file__'))


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)

    user_role = db.relationship('User', backref='role')

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()


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
    name = db.Column(db.String(64))
    location = db.Column(db.String(64))
    about_me = db.Column(db.Text())
    member_since = db.Column(db.DateTime, default=datetime.now)
    last_seen = db.Column(db.DateTime, default=datetime.now)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    users = db.relationship('Role', backref='users')
    article = db.relationship('Articles', backref='author')
    question = db.relationship('Questions', backref='author')
    article_comment = db.relationship('ArticleComments', backref='reviewer')
    question_comment = db.relationship('QuestionComments', backref='reviewer')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
                self.role_id = self.role.id
                Thread(target=self.save_user_portrait()).start()
            else:
                self.role = Role.query.filter_by(default=True).first()
                self.role_id = self.role.id
                Thread(target=self.save_user_portrait()).start()

    def ping(self):
        self.last_seen = datetime.now()

    def can(self, permissions):
        """验证用户权限"""
        return self.role is not None and \
               (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        """判断用户是否是管理员"""
        return self.can(Permission.ADMINISTER)

    @property
    def password(self):
        """给User类添加属性"""
        return AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        """生成一个带时间限制的JSON WEB签名"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """验证令牌"""
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

    def generate_resetpwd_token(self, new_password, expiration=3600):
        """生成重置密码的令牌"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset': self.id,
                        'new_password': new_password})

    def reset_password(self, token):
        """验证修改密码令牌"""
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

    def generate_resetemail_token(self, new_email, expiration=3600):
        """生成重置密码的令牌"""
        s = Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'reset': self.id,
                        'new_email': new_email})

    def reset_email(self, token):
        """验证修改密码令牌"""
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data['reset'] != self.id:
            return False
        else:
            self.email = data['new_email']

            if self.email == current_app.config['FLASK_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
                self.role_id = self.role.id
                Thread(target=self.save_user_portrait()).start()
            else:
                self.role = Role.query.filter_by(default=True).first()
                self.role_id = self.role.id
                Thread(target=self.save_user_portrait()).start()

            return True

    def generate_portrait_url(self, size=100, default='identicon', rating='g'):
        """
        生成生成头像的url
        size范围：1 - 512px
        default参数：gravatar官方图形
                    404 直接返回404错误状态
                    mm 神秘人(一个灰白头像)
                    identicon 抽象几何图形
                    monsterid 小怪物
                    wavatar 用不同面孔和背景组合生成的头像
                    retro 八位像素复古头像
        rating头像等级：g 适合任何年龄的访客查看，一般都用这个
                       pg 可能有争议的头像，只适合13岁以上读者查看
                       r 成人级，只适合17岁以上成人查看
                       x 最高等级，不适合大多数人查看
        """

        # 判断请求是否安全
        if request.is_secure:
            url = 'https://secure.gravatar.com/avatar'
        else:
            url = 'http://www.gravatar.com/avatar'

        # url = 'https://secure.gravatar.com/avatar'
        email_hash = md5(self.email.encode('utf-8')).hexdigest()

        # 头像服务器/avatar/邮箱的md5值?s=头像尺寸&d=默认头像&r=头像等级
        # 如果需要强制显示默认头像，在最后加上参数&f=y
        return '{url}/{email_hash}?s={size}&d={default}&r={rating}'.format(
            url=url, email_hash=email_hash, size=size, default=default, rating=rating)

    def save_user_portrait(self):
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/61.0.3153.0 Safari/537.36'}

        # 从python中的上下文管理器导入
        from contextlib import closing

        # stream 开启文件流方式
        with closing(requests.get(self.generate_portrait_url(size=250), headers=headers, stream=True)) as response:

            f = BASE_PWD + '/app/static/images/user_portrait/{}.png'.format(self.username.encode('utf-8'))
            if os.path.exists(f):
                os.remove(f)

            with open(f, 'wb') as fw:
                # 每128个内容写一次
                for chunk in response.iter_content(128):
                    fw.write(chunk)

    def __repr__(self):
        return '[user: {}]'.format(self.username.encode('utf-8'))


@login_manager.user_loader
def load_user(user_id):
    """
    加载用户的回调函数,接收以Unicode字符串形式的用户标识
    """
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


class AnonymousUser(AnonymousUserMixin):
    """匿名用户登入"""

    def can(self, permissions):
        return False

    def is_administrator(self):
        return False


# 自定义匿名用户
login_manager.anonymous_user = AnonymousUser


class Classification(db.Model):
    __tablename__ = 'classification'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    class_name = db.Column(db.String(10), nullable=False)

    @staticmethod
    def add_classification():
        class_names = [u'技术', u'生活']
        for each in class_names:
            each_class = Classification(class_name=each)
            db.session.add(each_class)
            db.session.commit()


class Articles(db.Model):
    __tablename_ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_articles = db.relationship('User', backref=db.backref('user_articles', order_by=create_time.desc()))

    class_id = db.Column(db.Integer, db.ForeignKey('classification.id'))
    class_articles = db.relationship('Classification', backref='class_articles')


class Questions(db.Model):
    __tablename_ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(30), nullable=False)
    body = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, index=True)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user_questions = db.relationship('User', backref=db.backref('user_questions', order_by=create_time.desc()))

    class_id = db.Column(db.Integer, db.ForeignKey('classification.id'))
    class_questions = db.relationship('Classification', backref='class_questions')


class ArticleComments(db.Model):
    __tablename__ = 'article_comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, index=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    article_comments = db.relationship('Articles', backref='comments')


class QuestionComments(db.Model):
    __tablename__ = 'question_comments'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    body = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, index=True)

    reviewer_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'))
    question_comments = db.relationship('Questions', backref='comments')

class ArticlesCareTable(db.Model):
    __tablename__ = 'articles_care_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    care_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    care_article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    care_time = db.Column(db.DateTime, index=True)

    care_articles = db.relationship('User', backref=db.backref('care_articles', order_by=care_time.desc()))
    care_users = db.relationship('Articles', backref=db.backref('care_article_users', order_by=care_time.desc()))

class QuestionsCareTable(db.Model):
    __tablename__ = 'questions_care_table'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    care_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    care_question_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    care_time = db.Column(db.DateTime, index=True)

    care_questions = db.relationship('User', backref=db.backref('care_questions', order_by=care_time.desc()))
    care_users = db.relationship('Questions', backref=db.backref('care_question_users', order_by=care_time.desc()))