#!/usr/bin/python
# -*- coding: utf-8 -*-


def response_messages(response, title, content):
    """
    :param response: 返回给前端的dict
    :param title: 前端消息弹框的标题
    :param content: 前端消息弹框的内容
    """
    response['data']['message-title'] = title
    response['data']['message-content'] = content