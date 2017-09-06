#!/usr/bin/python
# -*- coding: utf-8 -*-

from . import auth
from .. import login_manager

login_manager.login_view = "auth.login"

@login_manager.user_loader
def load_user(user_id):
    return None

@auth.route('/login/')
def login():
    return 'test'
