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
import time

from haystack.nodes import EmbeddingRetriever
from haystack.document_stores.milvus import MilvusDocumentStore
# from android_recommend.haystack.milvus_document.milvus1 import Milvus1DocumentStore as MilvusDocumentStore

from util import PathUtil
from util import PreSufConstant
from util import FileUtil
from preprocessor.good2mysql.record_document import DocumentRecord


class MilvusRetrieval:
    def __init__(self, db_name, index_name, model_name,
                 embedding_dim, doc_simi='cosine',
                 mysql_config_path=PathUtil.mysql_config_path(),
                 milvus_config_path=PathUtil.milvus_config_path(),
                 ):
        self.index = f'{PreSufConstant.DB_INDEX_PREFIX_MILVUS}{index_name}{PreSufConstant.DB_INDEX_SUFFIX}'
        self.model_path = PathUtil.saved_models(model_name)
        self.sql_url = self._generate_sql_url(mysql_config_path, db_name)
        self.milvus_url = self._generate_milvus_url(milvus_config_path)
        self.embedding_dim = embedding_dim
        self.similarity = doc_simi

        self.document_store: MilvusDocumentStore = MilvusDocumentStore(
            sql_url=self.sql_url,
            milvus_url=self.milvus_url,
            embedding_dim=self.embedding_dim,
            index=self.index,
            similarity=self.similarity,
            duplicate_documents='skip'
        )
        self.retriever: EmbeddingRetriever = EmbeddingRetriever(
            document_store=self.document_store,
            embedding_model=self.model_path,  # model_path or name in hugging Face
            model_format='sentence_transformers'
        )

    # def __del__(self):
    #     self.

    def write_document(self, documents, batch_size=500):
        start_time = time.time()
        self.document_store.write_documents(
            documents=documents,
            index=self.index,
            batch_size=batch_size,
            duplicate_documents='skip'
        )
        end_time = time.time()
        print("Write documents finish in %f s." % (end_time - start_time))

    def update_embedding(self, batch_size=64):
        start_time = time.time()
        self.document_store.update_embeddings(
            retriever=self.retriever,
            index=self.index,
            update_existing_embeddings=True,
            batch_size=batch_size
        )
        end_time = time.time()
        print("Update embeddings in the document_store store according to retriever in %f s." % (
                end_time - start_time))

    @staticmethod
    def _generate_sql_url(mysql_config_path, db_name):
        mysql_list = FileUtil.load_data_list(mysql_config_path)
        if len(mysql_list) == 0:
            return None
        mysql_data = mysql_list[0]
        db = '{}{}{}'.format(PreSufConstant.DB_NAME_PREFIX_MILVUS, db_name, PreSufConstant.DB_NAME_SUFFIX)
        sql_url = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8mb4'.format(
            mysql_data.get('user', ''),
            mysql_data.get('password', ''),
            mysql_data.get('host', ''),
            mysql_data.get('port', ''),
            db
        )
        return sql_url

    @staticmethod
    def _generate_milvus_url(milvus_config_path):
        milvus_list = FileUtil.load_data_list(milvus_config_path)
        if len(milvus_list) == 0:
            return None
        milvus_data = milvus_list[0]
        milvus_url = f"tcp://{milvus_data.get('host', '')}:{milvus_data.get('port', '')}"
        return milvus_url

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
        self.write_document(documents)
        self.update_embedding()
        DocumentRecord.update_record(documents, self.retrieval_id)

    def delete_doc(self):
        self.document_store.delete_all_documents()
        # clean DocRecord
        DocumentRecord.remove_all_record(self.retrieval_id)
