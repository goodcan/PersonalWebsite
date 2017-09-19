#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

main = Blueprint('main', __name__)

from . import views, errors
from ..models import Permission

@main.app_context_processor
def inject_permissions():
    """添加上下文可以在模板中使用"""
    return dict(Permission=Permission)