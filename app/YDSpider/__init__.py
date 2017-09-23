#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Blueprint

trans = Blueprint('trans', __name__)

from . import views