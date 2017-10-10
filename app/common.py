#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import url_for
from datetime import datetime

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


class MakeLoadDate:
    @staticmethod
    def some_article_data(obj):
        """不带头像连接"""
        author = obj.author
        load_data = {
            'id': obj.id,
            'user_portrait_url': url_for('static', filename='images/user_portrait/' + author.username + '.png'),
            'title': obj.title,
            'title_link': url_for('auth.detail_article', article_id=obj.id),
            'create_time': str(obj.show_create_time),
            'body': obj.body,
            'comment_link': url_for('auth.detail_article', article_id=obj.id),
            'comment_num': len(obj.comments),
            'care_num': len(obj.care_article_users)
        }

        return load_data

    @staticmethod
    def some_question_data(obj):
        """不带头像连接"""
        author = obj.author
        load_data = {
            'id': obj.id,
            'user_portrait_url': url_for('static', filename='images/user_portrait/' + author.username + '.png'),
            'title': obj.title,
            'title_link': url_for('auth.detail_question', question_id=obj.id),
            'create_time': str(obj.show_create_time),
            'body': obj.body,
            'comment_link': url_for('auth.detail_question', question_id=obj.id),
            'comment_num': len(obj.comments),
            'care_num': len(obj.care_question_users)
        }

        return load_data

    @classmethod
    def all_article_data(cls, obj):
        """带头像连接"""
        load_data = cls.some_article_data(obj)
        author = obj.author
        load_data['user_portrait_link'] = url_for('auth.user_index', username=author.username)

        return load_data

    @classmethod
    def all_question_data(cls, obj):
        """带头像连接"""
        load_data = cls.some_question_data(obj)
        author = obj.author
        load_data['user_portrait_link'] = url_for('auth.user_index', username=author.username)

        return load_data

    @staticmethod
    def comment(obj):
        """ ajax 请求评论数据"""
        reviewer = obj.reviewer
        if reviewer.name == None:
            name = reviewer.username
        else:
            name = reviewer.name

        load_data = {
            'user_portrait_link': url_for('auth.user_index', username=reviewer.username),
            'user_portrait_url': url_for('static', filename='images/user_portrait/' + reviewer.username + '.png'),
            'name': name,
            'create_time': str(obj.show_create_time),
            'body': obj.body
        }

        return load_data

    @staticmethod
    def comments_and_care_num_dict(articles, questions):
        article_comments = {}
        article_care_num = {}
        for each in articles:
            article_comments[each] = len(each.comments)
            article_care_num[each] = len(each.care_article_users)
        question_comments = {}
        question_care_num = {}
        for each in questions:
            question_comments[each] = len(each.comments)
            question_care_num[each] = len(each.care_question_users)

        data = {
            'article_comments': article_comments,
            'question_comments': question_comments,
            'article_care_num': article_care_num,
            'question_care_num': question_care_num
        }

        return data

