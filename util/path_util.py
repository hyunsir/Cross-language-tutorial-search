# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: Lenovo
@Email: 21212010059@m.fudan.edu.cn
@Created: 2021/12/15
------------------------------------------
@Modify: 2021/12/15
------------------------------------------
@Description:
"""
from definitions import *
class PathUtil:

    @staticmethod
    def origin_data(data_dir: str, file_name: str):
        data_file_path = os.path.join(data_dir, 'origin_data', file_name)
        return data_file_path

    @staticmethod
    def document_store(data_dir, file_name: str):
        document_store_path = os.path.join(data_dir, 'document_store', file_name)
        return document_store_path

    @staticmethod
    def saved_models(model_name: str):
        saved_model = os.path.join(SAVED_MODELS_DIR, model_name)
        return saved_model

    @staticmethod
    def mysql_config_path():
        mysql_config_path = os.path.join(ROOT_DIR, 'mysql_config.json')
        return mysql_config_path

    @staticmethod
    def milvus_config_path():
        milvus_config_path = os.path.join(ROOT_DIR, 'milvus_config.json')
        return milvus_config_path

    @staticmethod
    def es_config_path():
        milvus_config_path = os.path.join(ROOT_DIR, 'es_config.json')
        return milvus_config_path