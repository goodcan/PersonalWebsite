#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

#创建蓝本，第一个参数蓝本名字,第二个参数包或模块名
#在Python中在同一个文件里，__name__代表的是模块或包名
weather = Blueprint('weather', __name__)

#路由导入必须放在末尾，避免循环导入，因为在视图包需要导入main包
from . import views