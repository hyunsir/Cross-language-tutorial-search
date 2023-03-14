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
from haystack.document_stores import ElasticsearchDocumentStore
from haystack.nodes import ElasticsearchRetriever
from tutorial_recommend.util.constant_util import PreSufConstant
from tutorial_recommend.util.file_util import FileUtil
from preprocessor.good2mysql.record_document import DocumentRecord, RetrievalRecord
from definitions import Config


class ESRetrieval:
    def __init__(self, index_name, es_config_path=Config.es_config_DIR):
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
        self.retriever: ElasticsearchRetriever = ElasticsearchRetriever(
            document_store=self.document_store
        )

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

    def write_document_batch(self, documents, skip_num=0, batch_size=3000):
        documents = documents[skip_num:]
        batch_num = int(len(documents) / batch_size)
        print(f"Total data size {len(documents)}, split into {batch_num + 1} batches.")
        for i in range(batch_num):
            print(f"Write {format(i)} batch")
            data = documents[i * batch_size: (i + 1) * batch_size]
            self.write_document(data)
        print(f"Write {batch_num} batch")
        data = documents[batch_num * batch_size:]
        self.write_document(data)

    # def update_embedding(self, batch_size=64):
    #     try:
    #         start_time = time.time()
    #         self.document_store.update_embeddings(
    #             retriever=self.retriever,
    #             index=self.index,
    #             update_existing_embeddings=True,
    #             batch_size=batch_size
    #         )
    #         end_time = time.time()
    #         print("Update embeddings in the document_store store according to retriever in %f s." % (
    #                 end_time - start_time))
    #     except BaseException as e:
    #         print(e)

    def ask_one_query_api(self, query, retrieve_top_k=20):
        answer = self.retriever.retrieve(query=query, top_k=retrieve_top_k, index=self.index)
        return answer

    def ask_one_query_api_all_answer(self, query, retrieve_top_k=20):
        results = self.retriever.retrieve(query=query, top_k=retrieve_top_k, index=self.index)
        lines = DocumentRecord.retrieve_results2lines(results)
        for line in lines:
            print(line)
        return lines

    def get_retriever(self):
        return self.retriever

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
        self.write_document_batch(documents)
        # self.update_embedding()
        DocumentRecord.update_record(documents, self.retrieval_id)

    def just_update_record(self, documents):
        DocumentRecord.update_record(documents, self.retrieval_id)
