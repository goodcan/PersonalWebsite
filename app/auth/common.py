#!/usr/bin/python
# -*- coding: utf-8 -*

from flask import url_for
from flask_login import current_user
from .. import db
from ..common import response_messages


class DeleteContent(object):
    def make_response_data(self):
        re = {'status': True, 'data': {}}
        message_title = u'消息'
        message_content = u'删除成功！'
        response_messages(re, message_title, message_content)

        return re

    def delete_article(self, obj):
        about_comments = obj.comments
        if len(about_comments) != 0:
            for each in about_comments:
                db.session.delete(each)
        about_care = obj.care_article_users
        if len(about_care) != 0:
            for each in about_care:
                db.session.delete(each)
        db.session.delete(obj)
        db.session.commit()

        return self.make_response_data()

    def delete_question(self, obj):
        about_comments = obj.comments
        if len(about_comments) != 0:
            for each in about_comments:
                db.session.delete(each)
        about_care = obj.care_question_users
        if len(about_care) != 0:
            for each in about_care:
                db.session.delete(each)
        db.session.delete(obj)
        db.session.commit()

        return self.make_response_data()

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


class LoadPage(object):
    def __init__(self):
        self.pagination = None

    def make_index_pagination(self, page, re, db_obj, search_content, class_id):
        try:
            self.pagination = db_obj.query.filter(
                db_obj.title.like('%' + search_content.lower() + '%') if search_content is not None else '',
                db_obj.class_id.like('%' + class_id + '%')
            ).order_by(db_obj.create_time.desc()).paginate(page, per_page=10)
        except:
            re['status'] = False
            re['data']['message'] = u'已加载全部内容'

    def make_user_pagination(self, page, re, db_obj, user_id, class_id):
        try:
            self.pagination = db_obj.query.filter(
                db_obj.author_id.like('%' + user_id + '%'),
                db_obj.class_id.like('%' + class_id + '%')
            ).order_by(db_obj.create_time.desc()).paginate(page, per_page=10)
        except:
            re['status'] = False
            re['data']['message'] = u'已加载全部内容'

    def check_content(self, re, content):
        if not content:
            re['status'] = False
            re['data']['message'] = u'没有相关问答'

    def make_data(self, db_obj, re, content, pagination_obj):
        if re['status']:
            if db_obj.__name__ == 'Articles':
                for each in content:
                    re['data']['load_data'].append(MakeLoadDate.all_article_data(each))
                re['data']['next_page'] = pagination_obj.next_num
            elif db_obj.__name__ == 'Questions':
                for each in content:
                    re['data']['load_data'].append(MakeLoadDate.all_question_data(each))
                re['data']['next_page'] = pagination_obj.next_num

    def check_user(self, re, user_id):
        if current_user.is_authenticated and current_user.id == int(user_id):
            re['data']['same_user'] = True
        else:
            re['data']['same_user'] = False

    def index_search(self, page, db_obj, search_content, class_id):
        re = {'status': True, 'data': {'load_data': []}}
        self.make_index_pagination(page, re, db_obj, search_content, class_id)

        content = self.pagination.items
        print u'总页数:', self.pagination.pages

        self.check_content(re, content)

        self.make_data(db_obj, re, content, self.pagination)

        return re

    def user_screening(self, page, db_obj, user_id, class_id):
        re = {'status': True, 'data': {'load_data': []}}
        self.check_user(re, user_id)
        self.make_user_pagination(page, re, db_obj, user_id, class_id)

        content = self.pagination.items
        print u'总页数:', self.pagination.pages

        self.check_content(re, content)

        self.make_data(db_obj, re, content, self.pagination)

        return re
