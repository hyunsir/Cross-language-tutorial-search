# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/07/30
------------------------------------------
@Modify: 2022/07/30
------------------------------------------
@Description:
"""

import pymysql
from pymysql import OperationalError
from DBUtils.PooledDB import PooledDB  # pip install DBUtills==1.3
# sdkg web api  todo
from util.file_util import FileUtil
from definitions import Config

connection_config = FileUtil.load_data_list(Config.CONNECTION_CONFIG)


class DBName:
    ANDROID_RE = 'android_recommend_data'
    AUTO_SCRAPY = 'autoscrapy'


# 5为连接池里的最少连接数，setsession=['SET AUTOCOMMIT = 1']是用来设置线程池是否打开自动更新的配置，0为False，1为True
class Pools:
    conn_name_list = ['ali_0', 'in_89']
    pools_dict = {'ali_0': {}, 'in_89': {}}

    @staticmethod
    def check_db_in_connect(host, port, user, password, db_name):
        connection = pymysql.connect(host=host, port=port,
                                     user=user, password=password)
        try:
            with connection.cursor() as cursor:
                # 检查数据库是否存在
                cursor.execute(
                    f"SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name = '{db_name}';")
                result = cursor.fetchone()
                if result[0] == 0:
                    # 如果数据库不存在，则创建数据库
                    cursor.execute(
                        f"CREATE DATABASE {db_name} DEFAULT  CHARACTER SET  utf8mb4 DEFAULT COLLATE  utf8mb4_0900_ai_ci;;")
                    print(f"数据库 '{db_name}' 已创建.")
                else:
                    print(f"数据库 '{db_name}' 已存在.")
        finally:
            connection.close()

    @classmethod
    def init_ali_0(cls, db=DBName.ANDROID_RE):
        conf_ali0 = connection_config['ali_0']
        pool_ali0_android = PooledDB(pymysql, 5,
                                     host=conf_ali0['host'],
                                     port=conf_ali0['port'],
                                     user=conf_ali0['user'],
                                     passwd=conf_ali0['password'],
                                     db=db,
                                     setsession=['SET AUTOCOMMIT = 1'])
        cls.pools_dict['ali_0'][db] = pool_ali0_android

    @classmethod
    def init_in_89(cls, db=DBName.AUTO_SCRAPY):
        conf_in89 = connection_config['in_89']
        pool_in89_scrapy = PooledDB(pymysql, 5,
                                    host=conf_in89['host'],
                                    port=conf_in89['port'],
                                    user=conf_in89['user'],
                                    passwd=conf_in89['password'],
                                    db=db,
                                    setsession=['SET AUTOCOMMIT = 1'])
        cls.pools_dict['in_89'][db] = pool_in89_scrapy

    @classmethod
    def get(cls, conn_name, db):
        if conn_name not in cls.pools_dict:
            print("no such service")
            return None
        if (not db in cls.pools_dict[conn_name]) or (not cls.pools_dict[conn_name][db]):
            if conn_name == 'ali_0':
                cls.init_ali_0(db)
            elif conn_name == 'in_89':
                cls.init_in_89(db)
        return cls.pools_dict[conn_name][db]


class DataUploader:
    """
        与mysql表在init时候绑定的 传输器
    """

    def __init__(self, db_name, table, connection_name='ali_0'):
        self.db_name = db_name
        self.pool = Pools.get(connection_name, db_name)
        self.table = table
        self.columns, self.columns_type = self._get_column_names()  # 列名 列类型
        self.column_len = len(self.columns)
        self.col_is_str: list = self._get_col_is_str()

    def _get_col_is_str(self):
        col_is_str = []
        for type_num in self.columns_type:
            if type_num == 7 or (type_num > 9 and type_num not in [16, 246]):
                col_is_str.append(True)
            else:
                col_is_str.append(False)
        return col_is_str

    def _get_column_names(self):
        """
        在init调用，得到所有列名，按照select * 的列顺序
        :return: ['id','url','xxx',]
        """
        connection = self._get_connection()
        cursor = connection.cursor()
        sql = f'select * from {self.table} limit 0,1'
        cursor.execute(sql)
        desc = cursor.description
        connection.close()
        column_names = []
        columns_type = []
        for item in desc:
            column_names.append(item[0])
            columns_type.append(item[1])
        return column_names, columns_type

    def _get_connection(self):
        return self.pool.connection()

    def _execute_sql(self, sql):
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(sql)
            connection.commit()
        except OperationalError as e:
            print('_execute_sql error')
            connection.rollback()
            print(sql[0:50])
            print(e)
        connection.close()

    def _execute_many_sql(self, sql, values):
        connection = self._get_connection()
        cursor = connection.cursor()
        try:
            cursor.executemany(sql, values)
            connection.commit()
        except OperationalError as e:
            print('_execute_sql error')
            connection.rollback()
            print(sql[0:50])
            print(e)
        connection.close()

    def execute_sql_fetchall(self, sql):
        connection = self._get_connection()
        cursor = connection.cursor()
        datas = None
        try:
            cursor.execute(sql)
            connection.commit()
            datas = cursor.fetchall()
        except OperationalError as e:
            print('error')
            print(sql[0:50])
            connection.rollback()
            print(e)
        connection.close()
        return datas

    def get_max_id(self, id_name='id'):
        """
        如果id不在列名中，会返回空。
        :return: 最大id
        """
        if id_name not in self.columns:
            print('error！ id_name not in table columns')
            return None
        sql = f"select max({id_name}) from {self.table}"
        datas = self.execute_sql_fetchall(sql)
        max_id = datas[0][0]
        if not max_id:
            return 0
        return max_id

    def insert_all_values(self, sql_values):
        if len(sql_values) == 0:
            return
        if self.column_len != len(sql_values[0]):
            print('error! one line length not== table column length!')
            return
        data_str_list = []
        for line in sql_values:
            if type(line[0]) != str:
                line_str = str(line[0])
            else:
                line_str = "'" + line[0] + "'"
            for item in line[1:]:
                line_str += ','
                if type(item) != str:
                    line_str += str(item)
                else:
                    line_str += "'" + item + "'"
            line_str = '(' + line_str + ')'
            data_str_list.append(line_str)
        data_str = ','.join(data_str_list)
        # print(data_str)
        sql = f'''INSERT INTO {self.table} values {data_str};'''
        self._execute_sql(sql)

    def insert_execute_many(self, sql_values):
        if len(sql_values) == 0:
            return
        if self.column_len != len(sql_values[0]):
            print('error! one line length not== table column length!')
            return
        sql_str = ['%s'] * self.column_len
        sql_str = '(' + ','.join(sql_str) + ')'
        sql = f"INSERT INTO {self.table} values " + sql_str
        self._execute_many_sql(sql, sql_values)

    def insert_values_auto_id(self, sql_values):
        """
        数据已经对其，仅缺少最前一列id
        :param sql_values:
        :return:
        """
        print(f"insert {len(sql_values)} lines into {self.table}, auto adding id ")
        id = self.get_max_id() + 1
        id_values = []
        for line in sql_values:
            id_line = [id]
            id_line.extend(list(line))
            id_line = tuple(id_line)
            id_values.append(id_line)
            id += 1
        id_values = tuple(id_values)
        self.insert_all_values(id_values)

    def select_by_key_list(self, key_col_name, key_list):
        """
        :param key_col_name: 查询列名字
        :param key_list: 该列的查询内容
        :return: 经过整理的，跟输入查询列一一对应的数据
        """
        if key_col_name not in self.columns:
            print('error! no such col name!')
            return
        key_index = self.columns.index(key_col_name)  # key_index: 查询列在整体数据中的位置 从零开始计数
        if type(key_list[0]) == str:
            col_list_str = f'''"{key_list[0]}"'''
            for item in key_list[1:]:
                col_list_str += ',' + f'''"{item}"'''
        else:
            col_list_str = str(key_list[0])
            for item in key_list[1:]:
                col_list_str += ',' + str(item)
        sql = f'''select * from {self.table} where {key_col_name} in ({col_list_str})'''
        # print(sql)
        datas = self.execute_sql_fetchall(sql)
        if not datas:
            ret = []
            for i in range(len(key_list)):
                ret.append(None)
            return ret
        url2info = {}
        for data in datas:
            url2info[data[key_index]] = data
        info_list = []
        for _url in key_list:
            if _url in url2info:
                info_list.append(list(url2info[_url]))
            else:
                info_list.append(None)
        return info_list

    def select_all(self):
        sql = f'''select * from {self.table}'''
        datas = self.execute_sql_fetchall(sql)
        return datas

    def select_stream(self, sql):
        if not sql:
            sql = f'''select * from {self.table}'''
        connection = self._get_connection()
        cursor = connection.cursor(cursor=pymysql.cursors.SSCursor)
        try:
            cursor.execute(sql)
            while True:
                result = cursor.fetchone()
                if result:
                    yield result
                else:
                    break
        except:
            print('error in select_all_stream')
        cursor.close()
        connection.close()


class ABC:
    connection = None

    @classmethod
    def get(cls):
        if not cls.connection:
            cls.connection = 1
        print(cls.connection)
        return cls.connection

    @classmethod
    def __del__(cls):
        cls.connection = None
        print(cls.connection)


if __name__ == '__main__':
    # db_name = "android_recommend_data"
    # table = "issuetracker"
    # an_tutorial = DataUploader(db_name, table)
    # datas = an_tutorial.select_by_key_list('id', ["ds", 3])
    # print(datas)

    conf = connection_config['ali_0']
    conn = pymysql.connect(host=conf['host'], user=conf['user'], password=conf['password'], port=3307)
    cursor = conn.cursor()  # 创建游标
    sql = 'create database if not exists test_db;'  # 创建数据的sql语句
    cursor.execute(sql)
    conn.close()
