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
import json

class FileUtil:

    @staticmethod
    def load_data_list(file_path):
        index = file_path.rfind('.')
        file_type = file_path[index + 1:]
        if file_type == 'json':
            return FileUtil.load_data_list_from_json(file_path)
        if file_type == 'jl':
            return FileUtil.load_data_list_from_jl(file_path)

    @staticmethod
    def load_data_list_from_jl(jl_file_path):
        data_list = []
        with open(jl_file_path) as file:
            line = file.readline()
            while line != "":
                try:
                    data_list.append(json.loads(line))
                except BaseException as e:
                    print(e)
                    print("这行出错", line)
                line = file.readline()
        return data_list

    @staticmethod
    def load_data_list_from_json(json_file_path):
        with open(json_file_path, encoding='utf-8') as file:
            data_list = json.load(file)
        return data_list

    @staticmethod
    def save_data_list_from_json(file_path, data):
        with open(file_path, "w+", encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=4))
