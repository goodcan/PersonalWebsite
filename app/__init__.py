#!/usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from config import config


db = SQLAlchemy()
csrf = CSRFProtect()
mail = Mail()
login_manager = LoginManager()
# 'strong' 开启会话保护，会记录客户端IP地址和浏览器的用户代理信息
login_manager.session_protection = 'basic'
login_manager.login_view = "auth.login"



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)
    csrf.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from YDSpider import trans as trans_blueprint
    app.register_blueprint(trans_blueprint, url_prefix='/translation')

    return app
