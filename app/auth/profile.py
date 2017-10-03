#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from json import loads
from datetime import datetime
from . import auth
from .forms import ArticleForm, QuestionForm
from .. import db
from ..common import response_messages
from ..models import User, Articles, Questions, Classification, ArticleComments, QuestionComments


@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    user_articles = user.user_articles
    article_comments = {}
    for each in user_articles:
        article_comments[each] = len(each.comments)

    context = {
        'user': user,
        'article_comments': article_comments
    }
    return render_template('auth/user_profile.html', **context)


@auth.route('/user_index/<username>/')
def user_index(username):
    if current_user.username == username:
        return redirect(url_for('auth.user_profile', username=username))

    if current_user.is_authenticated:
        view_user = current_user
    else:
        view_user = None

    user = User.query.filter_by(username=username).first()
    user_articles = user.user_articles
    article_comments = {}
    for each in user_articles:
        article_comments[each] = len(each.comments)

    if user is None:
        abort(404)

    context = {
        'status': 0,  # user_navbar 状态标识
        'view_user': view_user,
        'user': user,
        'article_comments': article_comments
    }
    return render_template('auth/user_index.html', **context)


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
                           create_time=datetime.now(),
                           author_id=current_user.id,
                           class_id=class_id)

        db.session.add(article)
        db.session.commit()

        re = g.re
        message_title = u'消息'
        message_content = u'文章发布成功！'
        response_messages(re, message_title, message_content)

        re['load_data'] = {
            'user_portrait_url': url_for('static', filename='images/user_portrait/' + current_user.username + '.png'),
            'title': title,
            'title_link': url_for('auth.detail_article', article_id=article.id),
            'create_time': str(article.create_time),
            'body': body,
            'comment_link': url_for('auth.detail_article', article_id=article.id),
            'comment_num': 0,
            'care_num': 0
        }

        return jsonify(re)
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
                             create_time=datetime.now(),
                             author_id=current_user.id,
                             class_id=class_id)

        db.session.add(question)
        db.session.commit()

        re = g.re
        message_title = u'消息'
        message_content = u'提问成功！'
        response_messages(re, message_title, message_content)

        re['load_data'] = {
            'user_portrait_url': url_for('static', filename='images/user_portrait/' + current_user.username + '.png'),
            'title': title,
            'title_link': url_for('auth.detail_question', question_id=question.id),
            'create_time': str(question.create_time),
            'body': body,
            'comment_link': url_for('auth.detail_question', question_id=question.id),
            'comment_num': 0,
            'care_num': 0
        }

        return jsonify(re)
    else:
        g.re['status'] = False
        message_title = u'提问失败'
        message_content = ''
        for key, value in form.errors.items():
            print key + str(value)
            message_content += str(value[0]) + '<br>'

        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)


@auth.route('/detail_article/<article_id>/')
def detail_article(article_id):
    context = {
        'article': Articles.query.filter_by(id=article_id).first(),
        'article_comments': ArticleComments.query.filter_by(article_id=article_id).order_by('-create_time')
    }

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None

    return render_template('auth/detail_article.html', **context)


@auth.route('/detail_question/<question_id>/')
def detail_question(question_id):
    context = {
        'question': Questions.query.filter_by(id=question_id).first(),
        'question_comments': QuestionComments.query.filter_by(question_id=question_id).order_by('-create_time')
    }

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None

    return render_template('auth/detail_question.html', **context)


@auth.route('/add_article_comment/<article_id>', methods=['POST'])
def add_article_comment(article_id):
    g.re = {'status': True, 'data': {}}

    if not current_user.is_authenticated:
        g.re['status'] = False
        g.re['data']['url'] = url_for('auth.login') + \
                              '?next=%2Fauth%2Fdetail_article%2F' + article_id + '%2F'
        print g.re['data']['url']
        return jsonify(g.re)

    data = loads(request.get_data(), encoding='utf-8')
    print data

    body = data['data']['body']

    if body == '':
        g.re['status'] = False

        message_title = u'评论失败'
        message_content = u'评论内容不能为空！'
        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)

    article_comment = ArticleComments(body=body,
                                      create_time=datetime.now(),
                                      article_id=article_id,
                                      reviewer_id=current_user.id)

    db.session.add(article_comment)
    db.session.commit()

    re = g.re
    message_title = u'消息'
    message_content = u'评论成功！'
    response_messages(re, message_title, message_content)

    reviewer = article_comment.reviewer
    if reviewer.name == None:
        name = reviewer.username
    else:
        name = reviewer.name

    re['load_data'] = {
        'user_portrait_link': url_for('auth.user_index', username=reviewer.username),
        'user_portrait_url': url_for('static', filename='images/user_portrait/' + reviewer.username + '.png'),
        'name': name,
        'create_time': str(article_comment.create_time),
        'body': body
    }

    return jsonify(re)


@auth.route('/add_question_comment/<question_id>', methods=['POST'])
def add_question_comment(question_id):
    g.re = {'status': True, 'data': {}}

    if not current_user.is_authenticated:
        g.re['status'] = False
        g.re['data']['url'] = url_for('auth.login') + \
                              '?next=%2Fauth%2Fdetail_question%2F' + question_id + '%2F'
        print g.re['data']['url']
        return jsonify(g.re)

    data = loads(request.get_data(), encoding='utf-8')
    print data

    body = data['data']['body']

    if body == '':
        g.re['status'] = False

        message_title = u'评论失败'
        message_content = u'评论内容不能为空！'
        response_messages(g.re, message_title, message_content)

        return jsonify(g.re)

    question_comment = QuestionComments(body=body,
                                        create_time=datetime.now(),
                                        question_id=question_id,
                                        reviewer_id=current_user.id)

    db.session.add(question_comment)
    db.session.commit()

    re = g.re
    message_title = u'消息'
    message_content = u'评论成功！'
    response_messages(re, message_title, message_content)

    reviewer = question_comment.reviewer
    if reviewer.name == None:
        name = reviewer.username
    else:
        name = reviewer.name

    re['load_data'] = {
        'user_portrait_link': url_for('auth.user_index', username=reviewer.username),
        'user_portrait_url': url_for('static', filename='images/user_portrait/' + reviewer.username + '.png'),
        'name': name,
        'create_time': str(question_comment.create_time),
        'body': body
    }

    return jsonify(re)


@auth.route('/load_article/<article_id>/')
def load_article(article_id):
    pass
