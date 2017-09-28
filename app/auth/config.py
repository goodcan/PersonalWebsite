#!/usr/bin/python
# -*- coding: utf-8 -*-

from .. import login_manager

login_manager.session_protection = 'basic'
login_manager.login_view = "auth.login"