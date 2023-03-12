#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2021/12/09
------------------------------------------
@Modify: 2021/12/09
------------------------------------------
@Description:
"""
from flask import Flask
from app.module1.views import module1
from app.module2.views import module2


class Config(object):
    # 连接数据库
    # SQLALCHEMY_DATABASE_URI = ''
    # 绑定多个数据库 https://flask-sqlalchemy.palletsprojects.com/en/2.x/binds/#binds
    SQLALCHEMY_BINDS = {
        'module1': '',
        'module2': ''
    }
    # SQLAlchemy追踪对象的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 取消jsonify排序返回
    JSON_SORT_KEYS = False


def create_app():
    """
    注册蓝图并添加前缀 url_prefix
    :return: app
    """
    app = Flask(__name__)
    app.config.from_object(Config)
    # 挂载默认访问
    app.register_blueprint(module1)
    # 添加前缀
    # app.register_blueprint(module1, url_prefix="/module1")
    app.register_blueprint(module2, url_prefix="/module2")
    # 路由冲突时匹配第一个路由
    # app.register_blueprint(module2)
    return app
