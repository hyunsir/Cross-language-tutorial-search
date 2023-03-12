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
from util.db_util import db


class BaseModel2ORM(db.Model):
    # 数据库绑定
    __bind_key__ = 'module2'
    pass
