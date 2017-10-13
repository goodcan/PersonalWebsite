#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask_login import current_user
from datetime import datetime

def check_login():
    """检测是否有用户登入"""
    if current_user.is_authenticated:
        obj = current_user._get_current_object()
    else:
        obj = None

    return obj

def response_messages(response, title, content):
    """
    :param response: 返回给前端的dict
    :param title: 前端消息弹框的标题
    :param content: 前端消息弹框的内容
    """
    response['data']['message-title'] = title
    response['data']['message-content'] = content

def deal_time(start_time):
    end_time = datetime.now()
    if end_time >= start_time:
        D_value = end_time - start_time
    else:
        D_value = end_time - end_time

    if D_value.days > 0:
        if D_value.days >= 364:
            return start_time.strftime('%Y-%m-%d')

        if D_value.days > 5:
            return start_time.strftime('%m-%d %H:%M')

        return str(D_value.days) + u'天前'
    else:
        s = D_value.seconds
        h = s / 3600
        m = s % 3600 / 60
        # print s, h
        if h > 0:
            return str(h) + u'小时前'
        elif m > 0:
            return str(m) + u'分钟前'
        else:
            return u'刚刚'
