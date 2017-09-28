#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from json import loads
from . import auth
from .forms import ArticleForm, QuestionForm
from .. import db
from ..common import response_messages
from ..models import User, Articles, Questions, Classification


@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    context = {
        'user': user,
    }
    if user is None:
        abort(404)
    return render_template('auth/user_profile.html', **context)


@auth.route('/user_profile/add_article/', methods=['POST'])
def add_article():
    data = loads(request.get_data(), encoding='utf-8')
    print data
    g.re = {'status': True, 'data': {}}

    article_data = data['data']
    title = article_data['title']
    class_name = article_data['class_name']
    body = article_data['body']

    form = ArticleForm(title=title,
                       class_name=class_name,
                       body=body)

    if form.validate():
        class_id = Classification.query.filter_by(class_name=class_name).first().id

        article = Articles(title=title,
                           body=body,
                           author_id=current_user.id,
                           class_id=class_id)

        db.session.add(article)
        db.session.commit()

        message_title = u'消息'
        message_content = u'文章发布成功！'
        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)
    else:
        g.re['status'] = False
        message_title = u'发布失败'
        message_content = ''
        for key, value in form.errors.items():
            print key + str(value)
            message_content += str(value[0]) + '<br>'

        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)

@auth.route('/user_profile/add_question/', methods=['POST'])
def add_question():
    data = loads(request.get_data(), encoding='utf-8')
    print data
    g.re = {'status': True, 'data': {}}

    question_data = data['data']
    title = question_data['title']
    class_name = question_data['class_name']
    body = question_data['body']

    form = QuestionForm(title=title,
                       class_name=class_name,
                       body=body)

    if form.validate():
        class_id = Classification.query.filter_by(class_name=class_name).first().id

        question = Questions(title=title,
                           body=body,
                           author_id=current_user.id,
                           class_id=class_id)

        db.session.add(question)
        db.session.commit()

        message_title = u'消息'
        message_content = u'提问成功！'
        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)
    else:
        g.re['status'] = False
        message_title = u'提问失败'
        message_content = ''
        for key, value in form.errors.items():
            print key + str(value)
            message_content += str(value[0]) + '<br>'

        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)

@auth.route('/detail_article/<article_id>')
def detail_article(article_id):
    context = {}

    article = Articles.query.filter_by(id=article_id).first()

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None

    context['article'] = article
    return render_template('auth/detail_article.html', **context)


@auth.route('/detail_question/<question_id>')
def detail_question(question_id):
    context = {}

    question = Questions.query.filter_by(id=question_id).first()

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None

    context['question'] = question
    return render_template('auth/detail_question.html', **context)
