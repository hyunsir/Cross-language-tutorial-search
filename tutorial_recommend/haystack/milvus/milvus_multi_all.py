# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/10/24
------------------------------------------
@Modify: 2022/10/24
------------------------------------------
@Description:
"""
# import pprint
# from mysql_connector.Constants import RetrId

from tutorial_recommend.load_docs.all_title.get_all_doc import get_all_doc, source_id2table
from tutorial_recommend.haystack.milvus.milvus_retrieval import MilvusRetrieval
import urllib3
urllib3.disable_warnings()

class TutorialAllDocMilvusRetrieval(MilvusRetrieval):
    def __init__(self,model_path):
        index_name = "tutorial_all_doc_so50w_xlm-roberta-base"  # milvus_tutorial_all_doc_so50w_haystack
        embedding_dim = 512
        self.retrieval_id = 20002
        super().__init__(index_name, model_path, embedding_dim)

    @staticmethod
    def load_documents():
        # load new document which not in document_record table
        ret = get_all_doc()
        return ret

if __name__ == '__main__':
    query = 'dp dip'
    op = TutorialAllDocMilvusRetrieval("xlm-roberta-base")

    # doc = [
    #     {"content": "java 判断两个字符串相等",
    #     'meta': {'id': 71128,
    #              'source_id': 1
    #              }},
    # ]
    op.update_new_document()
    doc = op.ask_one_query_api(query, 300)
    for d in doc:
        print(d.content, source_id2table[d.meta['source_id']])

