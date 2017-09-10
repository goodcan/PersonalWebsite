#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class Config:
    # 对session添加一个盐
    WTF_CSRF_ENABLED = True
    # WTF_CSRF_CHECK_DEFAULT =False
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DEBUG = True

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = '104200'
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
    HOST = '127.0.0.1'
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
