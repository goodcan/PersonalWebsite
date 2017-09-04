#!/usr/bin/python
# -*- coding: utf-8 -*-

class Config:
    pass


class DevelopmentConfig(Config):
    DEBUG = True


config = {
    'development': DevelopmentConfig,

    'default': DevelopmentConfig
}
