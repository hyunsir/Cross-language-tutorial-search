# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/05/14
------------------------------------------
@Modify: 2022/05/14
------------------------------------------
@Description:
"""

import logging

from android_recommend.util.path_util import PathUtil


class LogUtil:
    __is_console = False
    __log_level = logging.INFO
    __log_file = PathUtil.logs()
    __log_util = None

    @classmethod
    def set_log_util(cls, is_console=__is_console, log_level=__log_level, log_file=__log_file):
        cls.__log_util: LogUtil = LogUtil(is_console=is_console, log_level=log_level, log_file=log_file)

    @classmethod
    def get_log_util(cls):
        if cls.__log_util is None:
            cls.__log_util: LogUtil = LogUtil()
        return cls.__log_util

    def __init__(self, is_console=__is_console, log_level=__log_level, log_file=__log_file):
        self.logger = logging.getLogger(log_file)
        self.logger.setLevel(logging.INFO)
        fmt = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%m/%d/%Y %H:%M:%S')

        if is_console:
            stream_handler = logging.StreamHandler()
            stream_handler.setFormatter(fmt)
            stream_handler.setLevel(log_level)
            self.logger.addHandler(stream_handler)

        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setFormatter(fmt)
        file_handler.setLevel(log_level)
        self.logger.addHandler(file_handler)

    def info(self, *msgs):
        for _ in msgs:
            self.logger.info(_)