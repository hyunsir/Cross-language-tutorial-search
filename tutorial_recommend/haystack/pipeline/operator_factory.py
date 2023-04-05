# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2023/04/03
------------------------------------------
@Modify: 2023/04/03
------------------------------------------
@Description:
"""
import time
from pathlib import Path

from haystack import Document
from haystack.nodes import JoinDocuments
from haystack.pipelines import Pipeline
from haystack.pipelines import TranslationWrapperPipeline
from haystack.nodes import TransformersTranslator


class PipeLine2R1K:
    def __init__(self, retrieval_milvus_op, retrieval_es_op, rerank):
        self.pipe = Pipeline()
        # pipe.add_node(component=QueryClassifier(), name="QueryClassifier", inputs=["Query"])
        self.pipe.add_node(component=retrieval_milvus_op.get_retriever(), name="MilvusRetriever", inputs=["Query"])
        self.pipe.add_node(component=retrieval_es_op.get_retriever(), name="ESRetriever", inputs=["Query"])
        self.pipe.add_node(component=JoinDocuments(join_mode="concatenate"), name="JoinResults",
                           inputs=["ESRetriever", "MilvusRetriever"])
        self.pipe.add_node(component=rerank, name="ranker", inputs=["JoinResults"])

    def run(self, query, retrieval_top_k, rerank_top_k):
        res = self.pipe.run(query=query, params={"ESRetriever": {"top_k": retrieval_top_k},
                                                 "MilvusRetriever": {"top_k": retrieval_top_k},
                                                 "ranker": {"top_k": rerank_top_k},
                                                 })
        return res


class TranslatorPipe:
    def __init__(self, pipeline):
        # pipeline = DocumentSearchPipeline(retriever=my_dpr_retriever)
        in_translator = TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-zh-en")
        out_translator = TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-en-zh")
        self.trans_pipeline = TranslationWrapperPipeline(input_translator=in_translator,
                                                         output_translator=out_translator,
                                                         pipeline=pipeline)

    def run(self, query, retrieval_top_k=30):
        res = self.trans_pipeline.run(query=query, params={"ESRetriever": {"top_k": retrieval_top_k}})
        return res


if __name__ == '__main__':
    from tutorial_recommend.haystack.es.es_multi_all import TutorialAllDocESRetrieval
    from tutorial_recommend.load_docs.all_title.get_all_doc import source_id2table

    # time0 = time.time()
    # pipe = Pipeline()
    # pipe.add_node(component=TutorialAllDocESRetrieval().get_retriever(), name="ESRetriever", inputs=["Query"])
    # trans_pipe = TranslatorPipe(pipe)
    # time1 = time.time()
    # re = trans_pipe.run("convert csv to XML")
    # print(re)
    # for d in re['documents']:
    #     d: Document
    #     print(d.content, source_id2table[d.meta['source_id']])
    # time2 = time.time()
    # print(time1 - time0)
    # print(time2 - time1)

    time0 = time.time()
    pipeline = Pipeline.load_from_yaml(
        Path("D:/lab/Cross-language-tutorial-search/tutorial_recommend/haystack/pipeline/haystack-pipeline.yml"))
    time1 = time.time()
    re = pipeline.run("convert csv to XML",params={"ESRetriever50": {"top_k": 7}})
    print(re)
    for d in re['documents']:
        d: Document
        print(d.content, source_id2table[d.meta['source_id']])
    time2 = time.time()
    print(time1 - time0)
    print(time2 - time1)
