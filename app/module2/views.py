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
from flask import Blueprint

# 创建蓝图
module2 = Blueprint('module2', __name__)


@module2.route('/')
def index():
    return 'Hello Module2!'
