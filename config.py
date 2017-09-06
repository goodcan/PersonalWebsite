#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

class Config:
    # 对session添加一个盐
    SECRET_KEY = os.urandom(24)

class DevelopmentConfig(Config):
    DEBUG = True

    DIALECT = 'mysql'
    DRIVER = 'mysqldb'
    USERNAME = 'root'
    PASSWORD = '104200'
    HOST = '127.0.0.1'
    PORT = '3306'
    DATABASE = 'blog'

    SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(
        DIALECT, DRIVER, USERNAME, PASSWORD, HOST, PORT, DATABASE
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
