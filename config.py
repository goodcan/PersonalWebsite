#!/usr/bin/python
# -*- coding: utf-8 -*-

import os


class Config:
    # 对session添加一个盐
    SECRET_KEY = os.urandom(24)
    # 开启csrf保护
    WTF_CSRF_ENABLED = True

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    FLASK_MAIL_SUBJECT_PREFIX = u'[灿灿]'
    FLASK_MAIL_SENDER = u'灿灿 <dt119971888@163.com>'
    FLASK_ADMIN = os.environ.get('FLASK_ADMIN')


class DevelopmentConfig(Config):
    DEBUG = True

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = '104200'
    # HOST = '101.132.123.153'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'my_website'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )


class TestingConfig(Config):
    TESTING = True

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = '104200'
    HOST = '101.132.123.153'
    PORT = '3306'
    DATABASE = 'my_website_test'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,

    'default': DevelopmentConfig
}
