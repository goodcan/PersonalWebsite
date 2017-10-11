#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, render_template
from flask_login import current_user
from . import auth
from ..common import MakeLoadDate
from ..models import Articles, Questions, CLASSIFICATION

@auth.route('/index/')
def index():
    context = {}

    articles = Articles.query.order_by(Articles.create_time.desc()).paginate(1, per_page=10).items
    questions = Questions.query.order_by(Questions.create_time.desc()).paginate(1, per_page=10).items

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
    re = {'status': True, 'data': {'load_data': []}}

    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    project_name = request.args.get('project_name')
    class_name = request.args.get('class_name')
    search_content = request.args.get('search_content')

    print project_name, class_name, search_content

    if project_name == u'文章':
        try:
            A_pagination = Articles.query.filter(
                Articles.title.like('%' + search_content.lower() + '%') if search_content is not None else '',
                Articles.class_id.like('%' + CLASSIFICATION[class_name] + '%')
            ).order_by(Articles.create_time.desc()).paginate(page, per_page=10)
        except:
            re['status'] = False
            re['data']['message'] = u'已加载全部内容'
            return jsonify(re)

        show_articles = A_pagination.items
        print u'总页数:', A_pagination.pages

        if not show_articles:
            re['status'] = False
            re['data']['message'] = u'没有相关文章'
            return jsonify(re)

        for each in show_articles:
            re['data']['load_data'].append(MakeLoadDate.all_article_data(each))
        re['data']['next_page'] = A_pagination.next_num
    else:
        try:
            Q_pagination = Questions.query.filter(
                Questions.title.like('%' + search_content.lower() + '%') if search_content is not None else '',
                Questions.class_id.like('%' + CLASSIFICATION[class_name] + '%')
            ).order_by(Questions.create_time.desc()).paginate(page, per_page=10)
        except:
            re['status'] = False
            re['data']['message'] = u'已加载全部内容'
            return jsonify(re)

        show_questions = Q_pagination.items
        print u'总页数:', Q_pagination.pages

        if not show_questions:
            re['status'] = False
            re['data']['message'] = u'没有相关问答'
            return jsonify(re)

        for each in show_questions:
            re['data']['load_data'].append(MakeLoadDate.all_question_data(each))
        re['data']['next_page'] = Q_pagination.next_num

    return jsonify(re)