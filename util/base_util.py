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
from flask import jsonify


class BaseUtil:
    @staticmethod
    def response(code, message, data=None):
        return jsonify({'code': code, 'message': message, 'data': data})
