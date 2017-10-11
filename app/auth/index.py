#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import jsonify, request, render_template, abort
from flask_login import current_user
from . import auth
from .common import MakeLoadDate
from .globalVariable import LOADPAGINATION
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
    print 'search page:', request.args.get('page')

    page = int(request.args.get('page'))
    project_name = request.args.get('project_name')
    class_name = request.args.get('class_name')
    search_content = request.args.get('search_content')

    print project_name, class_name, search_content

    if project_name == u'文章':
        re = LOADPAGINATION.index_search(page=page,
                             db_obj=Articles,
                             search_content=search_content,
                             class_id=CLASSIFICATION[class_name])

    else:
        re = LOADPAGINATION.index_search(page=page,
                             db_obj=Questions,
                             search_content=search_content,
                             class_id=CLASSIFICATION[class_name])

    return jsonify(re)
