# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2023/03/21
------------------------------------------
@Modify: 2023/03/21
------------------------------------------
@Description:
"""
from typing import Dict

from definitions import TABLE_LIST
from util.file_util import FileUtil
from mysql_connector.DataMysqlUploader import DataUploader

json_datas = FileUtil.load_data_list_from_json(TABLE_LIST)
source_id2table = {}
table2source_id = {}
for data in json_datas:
    source_id2table[data['source_id']] = data['table']
    table2source_id[data['table']] = data['source_id']


def get_all_doc():
    all_doc = []
    for data in json_datas:
        if data["IP"] == 0:
            connection_name = "ali_0"
        else:
            raise Exception(f'no IP named {data["IP"]}')
        db_name = data['db']
        table = data['table']
        columns = data['columns']
        source_id = data['source_id']
        condition = data['condition'] if 'condition' in data else None
        uploader = DataUploader(db_name, table, connection_name)
        sql = f"select {','.join(columns)} from {table} "
        if condition:
            sql += " where " + condition

        new_lines = uploader.execute_sql_fetchall(sql)
        new_doc = []
        for line in new_lines:
            id = line[0]
            title = line[1]

            index = title

            new_doc.append({
                "content": index,
                'meta': {'id': id,
                         'source_id': source_id
                         },
            })
        all_doc.extend(new_doc)
        print(f"new doc length: {len(new_doc)} in {table}")
        # print(new_doc[0:5])
    print(len(all_doc))
    return all_doc
