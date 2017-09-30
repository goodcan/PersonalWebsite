#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

starwar = Blueprint('starwar', __name__)

from . import views, sendData