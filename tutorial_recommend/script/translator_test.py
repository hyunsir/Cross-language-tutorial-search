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
from haystack import Document
from haystack.pipelines import TranslationWrapperPipeline, DocumentSearchPipeline
from haystack.nodes import TransformersTranslator
from haystack import Pipeline


DOCS = [
        Document(
            content="""Heinz von Foerster was an Austrian American scientist
                  combining physics and philosophy, and widely attributed
                  as the originator of Second-order cybernetics."""
        )
    ]
translator = TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-en-zh")
res = translator.translate(documents=DOCS, query=None)
print(res[0].content)


#
# pipeline = DocumentSearchPipeline(retriever=my_dpr_retriever)
# in_translator = TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-zh-en")
# out_translator = TransformersTranslator(model_name_or_path="Helsinki-NLP/opus-mt-en-zh")
# pipeline_with_translation = TranslationWrapperPipeline(input_translator=in_translator,
#                                                        output_translator=out_translator,
#                                                        pipeline=pipeline)