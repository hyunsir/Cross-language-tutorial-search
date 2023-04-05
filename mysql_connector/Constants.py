# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/09/16
------------------------------------------
@Modify: 2022/09/16
------------------------------------------
@Description:
"""


class ConnectName:
    in_89 = 'in_89'
    ali_0 = 'ali_0'


class DBName:
    ANDROID_RE = 'android_recommend_data'
    AUTO_SCRAPY = 'autoscrapy'


class TableName:
    TUTOR_W3S = 'tutorial_w3s'
    TUTOR_BIRD = 'tutorial_bird'
    TUTOR_BOKEYUAN = 'tutorial_bokeyuan'
    TUTOR_CSDN = 'tutorial_csdn'
    TUTOR_JIANSHU = 'tutorial_jianshu'
    TUTOR_DS = 'tutorial_ds'
    TUTOR_SUB = 'sub_tutorial'
    ISSUE = 'issuetracker'

    HONOR_ASK = "honor_ask"
    HONOR_MSG = "honor_msg"
    HONOR_TOPIC = "honor_topic"

    RECORD_DOC = 'document_record'
    RECORD_SOURCE = 'source_record'
    RECORD_RETRIE = 'retrieval_record'

    SUB_CSDN = 'sub_csdn'

    def __init__(self, code):
        self.code = code

    def __repr__(self):
        return self.code

    def __eq__(self, other):
        if isinstance(other, str):
            return self.code == other

        return isinstance(other, self.__class__) and self.code == other.code

    def __ne__(self, other):
        return self != other


class TableID:
    CSDN = 1
    W3S = 2
    BIRD = 3
    BOKEYUAN = 4
    DS = 5
    JIANSHU = 6
    ISSUE = 7
    DS_SUB = 8

    HONOR_ASK = 100
    HONOR_MSG = 101
    HONOR_TOPIC = 102


class RetrName:
    EN = 'en'
    CN = 'cn'
    EN_PASS = 'en_passage'
    CN_PASS = 'cn_passage'
    ISSUE = 'issue'

    ES_EN = 'es_en'
    ES_CN = 'es_cn'
    ES_EN_PASS = 'es_en_passage'
    ES_CN_PASS = 'es_cn_passage'
    ES_ISSUE = 'es_issue'

    HONOR = 'honor'


class RetrId:
    EN = 1
    CN = 2
    EN_PASS = 3
    CN_PASS = 4
    ISSUE = 5

    ES_EN = 6
    ES_CN = 7
    ES_EN_PASS = 8
    ES_CN_PASS = 9
    ES_ISSUE = 10

    HONOR = 100
    ES_HONOR = 101


class DataSourceType:
    pass


if __name__ == '__main__':
    print(TableName.TUTOR_CSDN)
