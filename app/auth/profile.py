#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from json import loads
from datetime import datetime
from time import sleep
from . import auth
from .forms import ArticleForm, QuestionForm
from .. import db
from ..common import response_messages
from ..models import User, Articles, Questions, Classification, ArticleComments, QuestionComments, ArticlesCareTable, \
    QuestionsCareTable


@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    user_articles = user.user_articles
    article_comments = {}
    article_care_num = {}
    for each in user_articles:
        article_comments[each] = len(each.comments)
        article_care_num[each] = len(each.care_article_users)
    user_questions = user.user_questions
    question_comments = {}
    question_care_num = {}
    for each in user_questions:
        question_comments[each] = len(each.comments)
        question_care_num[each] = len(each.care_question_users)

    context = {
        'user': user,
        'article_comments': article_comments,
        'question_comments': question_comments,
        'article_care_num': article_care_num,
        'question_care_num': question_care_num
    }
    return render_template('auth/user_profile.html', **context)


@auth.route('/user_index/<username>/')
def user_index(username):
    try:
        if current_user.username == username:
            return redirect(url_for('auth.user_profile', username=username))
    except:
        pass

    if current_user.is_authenticated:
        view_user = current_user
    else:
        view_user = None

    user = User.query.filter_by(username=username).first()
    user_articles = user.user_articles
    article_comments = {}
    article_care_num = {}
    for each in user_articles:
        article_comments[each] = len(each.comments)
        article_care_num[each] = len(each.care_article_users)
    user_questions = user.user_questions
    question_comments = {}
    question_care_num = {}
    for each in user_questions:
        question_comments[each] = len(each.comments)
        question_care_num[each] = len(each.care_question_users)

    if user is None:
        abort(404)

    context = {
        'status': 0,  # user_navbar 状态标识
        'view_user': view_user,
        'user': user,
        'article_comments': article_comments,
        'question_comments': question_comments,
        'article_care_num': article_care_num,
        'question_care_num': question_care_num
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
    article = Articles.query.filter_by(id=article_id).first()
    article_comments = ArticleComments.query.filter_by(article_id=article_id).order_by('-create_time')

    care = False
    if current_user.is_authenticated:
        if ArticlesCareTable.query.filter_by(care_user_id=current_user.id,
                                             care_article_id=article_id).first():
            care = True

    context = {
        'article': article,
        'article_comments': article_comments,
        'comment_num': len(article.comments),
        'care_num': len(article.care_article_users),
        'care': care
    }

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = {}
        context['user']['username'] = None

    return render_template('auth/detail_article.html', **context)


@auth.route('/detail_question/<question_id>/')
def detail_question(question_id):
    question = Questions.query.filter_by(id=question_id).first()
    question_comments = QuestionComments.query.filter_by(question_id=question_id).order_by('-create_time')

    care = False
    if current_user.is_authenticated:
        if QuestionsCareTable.query.filter_by(care_user_id=current_user.id,
                                             care_question_id=question_id).first():
            care = True

    context = {
        'question': question,
        'question_comments': question_comments,
        'comment_num': len(question.comments),
        'care_num': len(question.care_question_users),
        'care': care
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
        'body': body,
        'comment_num': len(Articles.query.filter_by(id=article_id).first().comments)
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
        'body': body,
        'comment_num': len(Questions.query.filter_by(id=question_id).first().comments)
    }

    return jsonify(re)


@auth.route('/screening_articles/<class_name>/<user_id>/')
def screening_articles(class_name, user_id):
    author_id = int(user_id)

    if class_name == u'全部':
        re = {'status': True, 'data': {'load_data': []}}
        articles = Articles.query.filter_by(author_id=user_id)
        for each in articles:
            author = each.author
            each_load_data = {
                'user_portrait_url': url_for('static',
                                             filename='images/user_portrait/' + author.username + '.png'),
                'title': each.title,
                'title_link': url_for('auth.detail_article', article_id=each.id),
                'create_time': str(each.create_time),
                'body': each.body,
                'comment_link': url_for('auth.detail_article', article_id=each.id),
                'comment_num': len(each.comments),
                'care_num': len(each.care_article_users)
            }

            re['data']['load_data'].append(each_load_data)

    if class_name != u'全部':
        re = {'status': True, 'data': {'load_data': []}}
        articles = Classification.query.filter_by(class_name=class_name).first().class_articles
        for each in articles:
            author = each.author
            if author.id == author_id:
                each_load_data = {
                    'user_portrait_url': url_for('static',
                                                 filename='images/user_portrait/' + author.username + '.png'),
                    'title': each.title,
                    'title_link': url_for('auth.detail_article', article_id=each.id),
                    'create_time': str(each.create_time),
                    'body': each.body,
                    'comment_link': url_for('auth.detail_article', article_id=each.id),
                    'comment_num': len(each.comments),
                    'care_num': len(each.care_article_users)
                }

                re['data']['load_data'].append(each_load_data)

    return jsonify(re)


@auth.route('/screening_questions/<class_name>/<user_id>/')
def screening_questions(class_name, user_id):
    author_id = int(user_id)

    if class_name == u'全部':
        re = {'status': True, 'data': {'load_data': []}}
        questions = Questions.query.filter_by(author_id=user_id)
        for each in questions:
            author = each.author
            each_load_data = {
                'user_portrait_url': url_for('static',
                                             filename='images/user_portrait/' + author.username + '.png'),
                'title': each.title,
                'title_link': url_for('auth.detail_question', question_id=each.id),
                'create_time': str(each.create_time),
                'body': each.body,
                'comment_link': url_for('auth.detail_question', question_id=each.id),
                'comment_num': len(each.comments),
                'care_num': len(each.care_question_users)
            }

            re['data']['load_data'].append(each_load_data)

    if class_name != u'全部':
        re = {'status': True, 'data': {'load_data': []}}
        questions = Classification.query.filter_by(class_name=class_name).first().class_questions
        for each in questions:
            author = each.author
            if author.id == author_id:
                each_load_data = {
                    'user_portrait_url': url_for('static',
                                                 filename='images/user_portrait/' + author.username + '.png'),
                    'title': each.title,
                    'title_link': url_for('auth.detail_question', question_id=each.id),
                    'create_time': str(each.create_time),
                    'body': each.body,
                    'comment_link': url_for('auth.detail_question', question_id=each.id),
                    'comment_num': len(each.comments),
                    'care_num': len(each.care_question_users)
                }

                re['data']['load_data'].append(each_load_data)

    return jsonify(re)


@auth.route('/care_article/<operation>/<article_id>/')
def care_article(operation, article_id):
    g.re = {'status': True, 'data': {}}

    if not current_user.is_authenticated:
        g.re['status'] = False
        g.re['data']['url'] = url_for('auth.login') + \
                              '?next=%2Fauth%2Fdetail_article%2F' + article_id + '%2F'
        print g.re['data']['url']
        return jsonify(g.re)

    if operation == 'add':
        article = ArticlesCareTable(care_user_id=current_user.id,
                                    care_article_id=article_id,
                                    care_time=datetime.now())
        db.session.add(article)
        db.session.commit()

        message_title = u'消息'
        message_content = u'关注成功！'
        response_messages(g.re, message_title, message_content)

    if operation == 'del':
        article = ArticlesCareTable.query.filter_by(care_user_id=current_user.id,
                                                    care_article_id=article_id).first()
        db.session.delete(article)
        db.session.commit()

        message_title = u'消息'
        message_content = u'取消关注成功！'
        response_messages(g.re, message_title, message_content)

    return jsonify(g.re)


@auth.route('/care_question/<operation>/<question_id>/')
def care_question(operation, question_id):
    g.re = {'status': True, 'data': {}}

    if not current_user.is_authenticated:
        g.re['status'] = False
        g.re['data']['url'] = url_for('auth.login') + \
                              '?next=%2Fauth%2Fdetail_question%2F' + question_id + '%2F'
        print g.re['data']['url']
        return jsonify(g.re)

    if operation == 'add':
        question = QuestionsCareTable(care_user_id=current_user.id,
                                    care_question_id=question_id,
                                    care_time=datetime.now())
        db.session.add(question)
        db.session.commit()

        message_title = u'消息'
        message_content = u'关注成功！'
        response_messages(g.re, message_title, message_content)

    if operation == 'del':
        question = QuestionsCareTable.query.filter_by(care_user_id=current_user.id,
                                                    care_question_id=question_id).first()
        db.session.delete(question)
        db.session.commit()

        message_title = u'消息'
        message_content = u'取消关注成功！'
        response_messages(g.re, message_title, message_content)

    return jsonify(g.re)

@auth.route('/check_article_care/<article_id>/')
def check_article_care(article_id):
    care = False
    if current_user.is_authenticated:
        if ArticlesCareTable.query.filter_by(care_user_id=current_user.id,
                                             care_article_id=article_id).first():
            care = True

    re = {'care': care}
    return jsonify(re)


@auth.route('/check_question_care/<question_id>/')
def check_question_care(question_id):
    care = False
    if current_user.is_authenticated:
        if QuestionsCareTable.query.filter_by(care_user_id=current_user.id,
                                             care_question_id=question_id).first():
            care = True

    re = {'care': care}
    return jsonify(re)

@auth.route('/update_article_care/<article_id>/')
def update_article_care(article_id):
    article = Articles.query.filter_by(id=article_id).first()
    if article:
        num = len(article.care_article_users)
    else:
        abort(404)

    re = {'num': num}
    return jsonify(re)

@auth.route('/update_question_care/<question_id>/')
def update_question_care(question_id):
    question = Questions.query.filter_by(id=question_id).first()
    if question:
        num = len(question.care_question_users)
    else:
        abort(404)

    re = {'num': num}
    return jsonify(re)

@auth.route('/user_care_content/')
def user_care_content():
    load_artilces = []
    articles_id = current_user.care_articles
    for each_id in articles_id:
        each = Articles.query.filter_by(id=each_id.care_article_id).first()
        author = each.author
        each_load_data = {
            'user_portrait_url': url_for('static',
                                         filename='images/user_portrait/' + author.username + '.png'),
            'title': each.title,
            'title_link': url_for('auth.detail_article', article_id=each.id),
            'create_time': str(each.create_time),
            'body': each.body,
            'comment_link': url_for('auth.detail_article', article_id=each.id),
            'comment_num': len(each.comments),
            'care_num': len(each.care_article_users)
        }
        load_artilces.append(each_load_data)

    load_questions = []
    questions_id = current_user.care_questions
    for each_id in questions_id:
        each = Questions.query.filter_by(id=each_id.care_question_id).first()
        author = each.author
        each_load_data = {
            'user_portrait_url': url_for('static',
                                         filename='images/user_portrait/' + author.username + '.png'),
            'title': each.title,
            'title_link': url_for('auth.detail_question', question_id=each.id),
            'create_time': str(each.create_time),
            'body': each.body,
            'comment_link': url_for('auth.detail_question', question_id=each.id),
            'comment_num': len(each.comments),
            'care_num': len(each.care_question_users)
        }
        load_questions.append(each_load_data)

    re = {'load_data': {
        'load_articles': load_artilces,
        'load_questions': load_questions
    }}

    return jsonify(re)
