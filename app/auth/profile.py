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
from ..common import response_messages, MakeLoadDate
from ..models import User, Articles, Questions, Classification, ArticleComments, QuestionComments, ArticlesCareTable, \
    QuestionsCareTable, CLASSIFICATION


@auth.route('/index/')
def index():
    context = {}

    articles = Articles.query.order_by(Articles.create_time.desc()).all()
    questions = Questions.query.order_by(Questions.create_time.desc()).all()

    context = {
        'articles': articles,
        'questions': questions,
    }
    context.update(MakeLoadDate.comments_and_care_num_dict(articles, questions))

    if current_user.is_authenticated:
        context['user'] = current_user
    else:
        context['user'] = None

    return render_template('auth/index.html', **context)


@auth.route('/index/search/')
def index_search():
    re = {'data': {'load_data': []}}
    project_name = request.args.get('project_name')
    class_name = request.args.get('class_name')
    search_content = request.args.get('search_content')
    print class_name, search_content

    if project_name == u'文章':
        if class_name == u'全部':
            all_articles = Articles.query.all()
        else:
            all_articles = Articles.query.filter_by(class_id=CLASSIFICATION[class_name]).all()

        for each in all_articles:
            if search_content != '':
                if search_content.lower() in each.title.lower():
                    re['data']['load_data'].append(MakeLoadDate.all_article_data(each))
            else:
                re['data']['load_data'].append(MakeLoadDate.all_article_data(each))
    else:
        if class_name == u'全部':
            all_questions = Questions.query.all()
        else:
            all_questions = Questions.query.filter_by(class_id=CLASSIFICATION[class_name]).all()

        for each in all_questions:
            if search_content != '':
                if search_content.lower() in each.title.lower():
                    re['data']['load_data'].append(MakeLoadDate.all_question_data(each))
            else:
                re['data']['load_data'].append(MakeLoadDate.all_question_data(each))

    return jsonify(re)


@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    user_articles = user.user_articles
    user_questions = user.user_questions

    context = MakeLoadDate.comments_and_care_num_dict(user_articles, user_questions)
    context['user'] = user

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
    user_questions = user.user_questions

    if user is None:
        abort(404)

    context = {
        'status': 0,  # user_navbar 状态标识
        'view_user': view_user,
        'user': user,
    }
    context.update(MakeLoadDate.comments_and_care_num_dict(user_articles, user_questions))

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

        re['load_data'] = MakeLoadDate.some_article_data(article)

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

        re['load_data'] = MakeLoadDate.some_question_data(question)

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
        context['user'] = None

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
        context['user'] = None

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

    all_comments = Articles.query.filter_by(id=article_id).first().comments
    re['comment_num'] = len(all_comments)
    re['load_data'] = []
    for each in all_comments:
        re['load_data'].append(MakeLoadDate.comment(each))

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

    all_comments = Questions.query.filter_by(id=question_id).first().comments
    re['comment_num'] = len(all_comments)
    re['load_data'] = []
    for each in all_comments:
        re['load_data'].append(MakeLoadDate.comment(each))

    return jsonify(re)


@auth.route('/screening_articles/<class_name>/<user_id>/')
def screening_articles(class_name, user_id):
    author_id = int(user_id)
    re = {'status': True, 'data': {'load_data': []}}

    if class_name == u'全部':
        articles = Articles.query.filter_by(author_id=user_id)
        for each in articles:
            re['data']['load_data'].append(MakeLoadDate.some_article_data(each))
    else:
        articles = Classification.query.filter_by(class_name=class_name).first().class_articles
        for each in articles:
            if each.author.id == author_id:
                re['data']['load_data'].append(MakeLoadDate.some_article_data(each))

    return jsonify(re)


@auth.route('/screening_questions/<class_name>/<user_id>/')
def screening_questions(class_name, user_id):
    author_id = int(user_id)
    re = {'status': True, 'data': {'load_data': []}}

    if class_name == u'全部':
        questions = Questions.query.filter_by(author_id=user_id)
        for each in questions:
            re['data']['load_data'].append(MakeLoadDate.some_question_data(each))
    else:
        questions = Classification.query.filter_by(class_name=class_name).first().class_questions
        for each in questions:
            if each.author.id == author_id:
                re['data']['load_data'].append(MakeLoadDate.some_question_data(each))

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
        load_artilces.append(MakeLoadDate.all_article_data(each))

    load_questions = []
    questions_id = current_user.care_questions
    for each_id in questions_id:
        each = Questions.query.filter_by(id=each_id.care_question_id).first()
        load_questions.append(MakeLoadDate.all_question_data(each))

    re = {'load_data': {
        'load_articles': load_artilces,
        'load_questions': load_questions
    }}

    return jsonify(re)
