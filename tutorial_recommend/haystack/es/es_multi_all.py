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
from tutorial_recommend.load_docs.all_title.get_all_doc import get_all_doc, source_id2table

from tutorial_recommend.haystack.es.es_retrieval import ESRetrieval
import urllib3
urllib3.disable_warnings()

class TutorialAllDocESRetrieval(ESRetrieval):
    def __init__(self):
        # 100w Write 596 batch
        index_name = "tutorial_all_doc_so50w"
        self.retrieval_id = 10002
        super().__init__(index_name)

    def load_documents(self):
        # load new document which not in document_record table
        ret = get_all_doc()
        return ret

if __name__ == '__main__':
    query = '如何把csv转换成XML？'
    op = TutorialAllDocESRetrieval()
    # doc = [
    #     {"content": "java 判断两个字符串相等",
    #     'meta': {'id': 71128,
    #              'source_id': 1
    #              }},
    # ]
    # AndroidCnMilvusRetrieval.update_embeddings()
    # answer = op.ask_one_query_api_all_answer(query)
    # op.update_new_document()
    doc = op.ask_one_query_api(query,10)
    for d in doc:
        print(d.content, source_id2table[d.meta['source_id']])
