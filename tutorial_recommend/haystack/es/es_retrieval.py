# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/11/07
------------------------------------------
@Modify: 2022/11/07
------------------------------------------
@Description:
"""
import time

from haystack import Pipeline
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import BM25Retriever
from util.constant_util import PreSufConstant
from util.file_util import FileUtil
# from preprocessor.good2mysql.record_document import DocumentRecord
from definitions import Config


class ESRetrieval:
    """
    haystack 提供了 document_store 和 retriever 两种基本的构件
    关于ES的两个构建有特定的构造方式 于是在这里又封装了一层
    ESRetrieval初始化后，提供对于document_store、retriever、pipeline的操作，不只是相应retriever
    """

    def __init__(self, index_name, es_config_path=Config.es_config_DIR):
        self.pipe = None
        self.index = f'{PreSufConstant.DB_NAME_PREFIX_ES}{index_name}{PreSufConstant.DB_INDEX_SUFFIX}'
        self.es_config = FileUtil.load_data_list(es_config_path)[0]
        self.document_store: ElasticsearchDocumentStore = ElasticsearchDocumentStore(
            host=self.es_config['host'],
            port=self.es_config['port'],
            username=self.es_config['username'],
            password=self.es_config['password'],
            scheme='https',
            verify_certs=False,
            index=self.index,
        )
        self.retriever: BM25Retriever = BM25Retriever(document_store=self.document_store)

    def write_document(self, documents, batch_size=1000):
        try:
            start_time = time.time()
            self.document_store.write_documents(
                documents=documents,
                index=self.index,
                batch_size=batch_size,
                duplicate_documents='skip'
            )
            end_time = time.time()
            print("Write documents finish in %f s." % (end_time - start_time))
        except BaseException as e:
            print(e)

    def ask_one_query_api(self, query, retrieve_top_k=20):
        return self.retriever.retrieve(query=query, top_k=retrieve_top_k, index=self.index)

    # def ask_one_query_api_all_answer(self, query, retrieve_top_k=20):
    #     results = self.retriever.retrieve(query=query, top_k=retrieve_top_k, index=self.index)
    #     lines = DocumentRecord.retrieve_results2lines(results)
    #     for line in lines:
    #         print(line)
    #     return lines

    def get_retriever(self):
        return self.retriever

    def get_pipeline(self):
        if not self.pipe:
            self.pipe = Pipeline()
            self.pipe.add_node(component=self.retriever, name="ESRetriever", inputs=["Query"])
        return self.pipe

    @staticmethod
    def load_documents():
        return []

    def update_new_document(self, documents=None):
        if not documents:
            documents = self.load_documents()
        if not self.retrieval_id:
            print('retrieval_id should be init')
            return
        if not documents:
            print(f'nothing should be updated in {self.retrieval_id}')
            return
        self.write_document(documents)
        # self.update_embedding()
        # DocumentRecord.update_record(documents, self.retrieval_id)

    # def just_update_record(self, documents):
    #     DocumentRecord.update_record(documents, self.retrieval_id)
