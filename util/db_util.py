#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2021/12/16
------------------------------------------
@Modify: 2021/12/16
------------------------------------------
@Description:
"""
from flask_sqlalchemy import SQLAlchemy

# 在项目注册多个蓝图的情况下统一实例化db对象
db = SQLAlchemy()
