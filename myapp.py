# coding=utf-8
import os

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from config import config

CONFIG_NAME = os.getenv('FLASK_CONFIG') or 'default'
app = Flask(__name__)
app.config.from_object(config[CONFIG_NAME])
config[CONFIG_NAME].init_app(app)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.session_protection = 'strong'
login_manager.login_message = u'请先登录'
login_manager.login_view = 'index'

if not app.debug and not app.config['SSL_DISABLE']:
    from flask.ext.sslify import SSLify
    sslify = SSLify(app)
