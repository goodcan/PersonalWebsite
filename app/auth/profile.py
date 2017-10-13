#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import g, jsonify, request, render_template, abort, redirect, url_for
from flask_login import login_required, current_user
from json import loads
from datetime import datetime
from . import auth
from .forms import ArticleForm, QuestionForm
from .. import db
from .common import MakeLoadDate
from .globalVariable import LOADPAGINATION, DELETE
from ..common import response_messages, check_login
from ..models import User, Articles, Questions, Classification, ArticleComments, QuestionComments, ArticlesCareTable, \
    QuestionsCareTable, CLASSIFICATION


@auth.route('/user_profile/<username>/')
@login_required
def user_profile(username):
    # 防止登录后其他账号直接伪登录
    if current_user.username != username:
        return redirect(url_for('auth.login'))

    user = User.query.filter_by(username=username).first()
    user_articles = Articles.query.filter_by(author_id=user.id) \
        .order_by(Articles.create_time.desc()).paginate(1, 10).items
    user_questions = Questions.query.filter_by(author_id=user.id) \
        .order_by(Questions.create_time.desc()).paginate(1, 10).items

    context = {
        'user': user,
        'add_delete_btn': True,
        'user_articles_num': len(user.user_articles),
        'user_questions_num': len(user.user_questions),
        'user_articles': user_articles,
        'user_questions': user_questions
    }

    context.update(MakeLoadDate.comments_and_care_num_dict(user_articles, user_questions))

    return render_template('auth/user_profile.html', **context)


@auth.route('/user_index/<username>/')
def user_index(username):
    try:
        if current_user.username == username:
            return redirect(url_for('auth.user_profile', username=username))
    except:
        pass

    user = User.query.filter_by(username=username).first()
    user_articles = Articles.query.filter_by(author_id=user.id) \
        .order_by(Articles.create_time.desc()).paginate(1, 10).items
    user_questions = Questions.query.filter_by(author_id=user.id) \
        .order_by(Questions.create_time.desc()).paginate(1, 10).items

    if user is None:
        abort(404)

    context = {
        'status': 0,  # user_navbar 状态标识
        'view_user': check_login(),
        'user': user,
        'user_articles_num': len(user.user_articles),
        'user_questions_num': len(user.user_questions),
        'add_delete_btn': False,
        'user_articles': user_articles,
        'user_questions': user_questions
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

        response_messages(re, title=u'消息', content=u'文章发布成功！')

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

        response_messages(re, title=u'消息', content=u'提问成功！')

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
    article_comments = ArticleComments.query.filter_by(article_id=article_id) \
        .order_by('-create_time').paginate(1, 10).items

    care = False
    if current_user.is_authenticated:
        if ArticlesCareTable.query.filter_by(care_user_id=current_user.id,
                                             care_article_id=article_id).first():
            care = True

    context = {
        'user': check_login(),
        'article': article,
        'article_comments': article_comments,
        'comment_num': len(article.comments),
        'care_num': len(article.care_article_users),
        'care': care
    }

    return render_template('auth/detail_article.html', **context)


@auth.route('/detail_question/<question_id>/')
def detail_question(question_id):
    question = Questions.query.filter_by(id=question_id).first()
    question_comments = QuestionComments.query.filter_by(question_id=question_id)\
        .order_by('-create_time').paginate(1, 10).items

    care = False
    if current_user.is_authenticated:
        if QuestionsCareTable.query.filter_by(care_user_id=current_user.id,
                                              care_question_id=question_id).first():
            care = True

    context = {
        'user': check_login(),
        'question': question,
        'question_comments': question_comments,
        'comment_num': len(question.comments),
        'care_num': len(question.care_question_users),
        'care': care
    }

    return render_template('auth/detail_question.html', **context)


@auth.route('/add_article_comment/', methods=['POST'])
def add_article_comment():
    re = {'status': True, 'data': {}}

    data = loads(request.get_data(), encoding='utf-8')
    print data

    article_id = data['data']['article_id']
    body = data['data']['body']

    if not current_user.is_authenticated:
        re['status'] = False
        re['data']['url'] = url_for('auth.login') + \
                            '?next=%2Fauth%2Fdetail_article%2F' + article_id + '%2F'
        print re['data']['url']
        return jsonify(re)

    if body == '':
        re['status'] = False

        response_messages(re, title=u'评论失败', content=u'评论内容不能为空！')

        return jsonify(re)

    article_comment = ArticleComments(body=body,
                                      create_time=datetime.now(),
                                      article_id=article_id,
                                      reviewer_id=current_user.id)

    db.session.add(article_comment)
    db.session.commit()

    response_messages(re, title=u'消息', content=u'评论成功！')

    # all_comments = Articles.query.filter_by(id=article_id).first().comments
    all_comments = ArticleComments.query.filter(ArticleComments.article_id == article_id) \
        .order_by(ArticleComments.create_time.desc()).paginate(1, 10).items
    load_data = []
    for each in all_comments:
        load_data.append(MakeLoadDate.comment(each))

    re.update({'comment_num': len(all_comments),
               'load_data': load_data})

    return jsonify(re)


@auth.route('/add_question_comment/<question_id>', methods=['POST'])
def add_question_comment(question_id):
    re = {'status': True, 'data': {}}

    if not current_user.is_authenticated:
        re['status'] = False
        re['data']['url'] = url_for('auth.login') + \
                            '?next=%2Fauth%2Fdetail_question%2F' + question_id + '%2F'
        print re['data']['url']
        return jsonify(re)

    data = loads(request.get_data(), encoding='utf-8')
    print data

    body = data['data']['body']

    if body == '':
        re['status'] = False

        message_title = u'评论失败'
        message_content = u'评论内容不能为空！'
        response_messages(re, message_title, message_content)

        return jsonify(re)

    question_comment = QuestionComments(body=body,
                                        create_time=datetime.now(),
                                        question_id=question_id,
                                        reviewer_id=current_user.id)

    db.session.add(question_comment)
    db.session.commit()

    response_messages(re, title=u'消息', content=u'评论成功！')

    # all_comments = Questions.query.filter_by(id=question_id).first().comments
    all_comments = QuestionComments.query.filter(QuestionComments.question_id == question_id) \
        .order_by(QuestionComments.create_time.desc()).paginate(1, 10).items
    load_data = []
    for each in all_comments:
        load_data.append(MakeLoadDate.comment(each))

    re.update({'comment_num': len(all_comments),
               'load_data': load_data})

    return jsonify(re)


@auth.route('/load_article_comment_page/')
def load_article_comment_page():
    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    article_id = request.args.get('article_id')

    re = LOADPAGINATION.comment_search(page=page,
                                       db_obj=ArticleComments,
                                       obj_id=article_id)
    return jsonify(re)

@auth.route('/load_question_comment_page/')
def load_question_comment_page():
    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    question_id = request.args.get('question_id')

    re = LOADPAGINATION.comment_search(page=page,
                                       db_obj=QuestionComments,
                                       obj_id=question_id)
    return jsonify(re)


@auth.route('/screening_articles/')
def screening_articles():
    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    class_name = request.args.get('class_name')
    user_id = request.args.get('user_id')

    print class_name, user_id

    re = LOADPAGINATION.user_screening(page=page,
                                       db_obj=Articles,
                                       user_id=user_id,
                                       class_id=CLASSIFICATION[class_name])

    return jsonify(re)


@auth.route('/screening_questions/')
def screening_questions():
    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    class_name = request.args.get('class_name')
    user_id = request.args.get('user_id')

    print class_name, user_id

    re = LOADPAGINATION.user_screening(page=page,
                                       db_obj=Questions,
                                       user_id=user_id,
                                       class_id=CLASSIFICATION[class_name])

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

        response_messages(g.re, title=u'消息', content=u'关注成功！')

    if operation == 'del':
        article = ArticlesCareTable.query.filter_by(care_user_id=current_user.id,
                                                    care_article_id=article_id).first()
        db.session.delete(article)
        db.session.commit()

        response_messages(g.re, title=u'消息', content=u'取消关注成功！')

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

        response_messages(g.re, title=u'消息', content=u'关注成功！')

    if operation == 'del':
        question = QuestionsCareTable.query.filter_by(care_user_id=current_user.id,
                                                      care_question_id=question_id).first()
        db.session.delete(question)
        db.session.commit()

        response_messages(g.re, title=u'消息', content=u'取消关注成功！')

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
        return abort(404)

    re = {'num': num}
    return jsonify(re)


@auth.route('/update_question_care/<question_id>/')
def update_question_care(question_id):
    question = Questions.query.filter_by(id=question_id).first()
    if question:
        num = len(question.care_question_users)
    else:
        return abort(404)

    re = {'num': num}
    return jsonify(re)


@auth.route('/user_care_articles/')
@login_required
def user_care_articles():
    page = int(request.args.get('page'))
    re = LOADPAGINATION.user_care_search(page=page,
                                         db_obj=ArticlesCareTable,
                                         user_id=current_user.id,
                                         load_db_obj=Articles)
    return jsonify(re)


@auth.route('/user_care_questions/')
@login_required
def user_care_questions():
    page = int(request.args.get('page'))
    re = LOADPAGINATION.user_care_search(page=page,
                                         db_obj=QuestionsCareTable,
                                         user_id=current_user.id,
                                         load_db_obj=Questions)
    return jsonify(re)


@auth.route('/delete_article/<article_id>/')
@login_required
def delete_article(article_id):
    article = Articles.query.filter_by(id=article_id, author_id=current_user.id).first()

    if not article:
        abort(400)

    re = DELETE.delete_article(article)

    return jsonify(re)


@auth.route('/delete_question/<question_id>/')
@login_required
def delete_question(question_id):
    question = Questions.query.filter_by(id=question_id, author_id=current_user.id).first()

    if not question:
        return abort(400)

    re = DELETE.delete_question(question)

    return jsonify(re)
