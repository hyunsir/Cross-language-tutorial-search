#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: duyi
@Email: yangty21@m.fudan.edu.cn
@Created: 2021/12/30
------------------------------------------
@Modify: 2021/12/30
------------------------------------------
@Description:
"""
import ssl

from elasticsearch import Elasticsearch
from ssl import create_default_context
import json
from tqdm import tqdm

from util.log_util import LogUtil
from util.path_util import PathUtil

logger = LogUtil.get_log_util()


class ElasticSearchUtile:
    def __init__(self, host, port, username=None, password=None):
        if username and password:
            ssl_context = create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            self.es = Elasticsearch(
                [f"https://{host}:{port}"],
                ssl_context=ssl_context,
                http_auth=(username, password),
                maxsize=15,
            )
        else:
            self.es = Elasticsearch(host + ':' + str(port), maxsize=15)
        logger.info(self.es.ping())

    def __create_index(self, index):
        """
        :param index: apikg => api
        :return:
        """
        if not self.es.indices.exists(index=index):
            try:
                self.es.indices.create(index=index)
            except Exception as e:
                logger.info(e.__class__.__name__, e)
        return index

    def generate_document(self, index, filename):
        index = self.__create_index(index)
        with open(PathUtil.api_data(f'{filename}.json'), 'r') as file:
            api_list = json.load(file)
        for api_item in tqdm(api_list):
            # if not self.es.exists(index=index, id=api_item['id']):
            try:
                self.es.index(index=index, document=api_item, id=api_item['id'])
            except Exception as e:
                logger.info(e.__class__.__name__, e)
            # else:
            #     logger.info('already exists')

    def __query_all_data(self, index, size):
        data = []
        try:
            res = self.es.search(index=index, size=size)
            for hit in res['hits']['hits']:
                data.append(hit['_source'])
        except Exception as e:
            logger.info(e.__class__.__name__, e)
        if not data:
            return None
        return data

    def __travel_es(self, **kwargs):
        # kwargs.setdefault("index", "api")
        kwargs.setdefault("body", {
            "query": {
                "match_al": {}
            }
        })
        # 存活时间
        kwargs.setdefault("scroll", "2m")
        kwargs.setdefault("size", 1000)
        res = self.es.search(**kwargs)
        scroll_id = res['_scroll_id']
        total_size = scroll_size = len(res['hits']['hits'])
        while scroll_size > 0:
            logger.info('Scrolling...')
            yield res['hits']['hits']
            res = self.es.scroll(scroll_id=scroll_id, scroll='2m')
            scroll_id = res['_scroll_id']
            scroll_size = len(res['hits']['hits'])
            total_size += scroll_size
            logger.info(f'already scrolled {total_size} items')

    def query_api_by_alias(self, alias, index='api'):
        query = {
            "bool": {
                "filter": [
                    {
                        "term": {
                            "alias": alias
                        }
                    }
                ]
            }
        }
        try:
            res = self.es.search(index=index, query=query)
            if not res:
                return None
            return res['hits']['hits'][0]['_source']
        except Exception as e:
            logger.info(e.__class__.__name__, e)

    def query_api_by_api_id(self, id, index='api'):
        query = {
            "bool": {
                "filter": [
                    {
                        "term": {
                            "api_id": id
                        }
                    }
                ]
            }
        }
        try:
            res = self.es.search(index=index, query=query)
            if not res:
                return None
            return res['hits']['hits'][0]['_source']
        except Exception as e:
            logger.info(e.__class__.__name__, e)

    def find_ids_by_label(self, labels: list, index='api'):
        # body = {
        #     "query": {
        #         "bool": {
        #             "filter": [
        #                 {
        #                     "term": {
        #                         f"labels.{label}": "true"
        #                     }
        #                 }
        #             ]
        #         }
        #     }
        # }
        labels_match = '#' + ' #'.join(labels)
        body = {
            "query": {
                "match": {
                    "labels": labels_match
                }
            }
        }
        match_list = []
        try:
            for res_item in self.__travel_es(index=index, body=body):
                match_list += [m['_source']['id'] for m in res_item]
            return match_list
        except Exception as e:
            logger.info(e.__class__.__name__)

    def find_node_ids_by_label(self, labels: list, index='api'):
        # TODO api_id >>> node_id
        labels_match = '#' + ' #'.join(labels)
        body = {
            "query": {
                "match": {
                    "labels": labels_match
                }
            }
        }
        match_set = set()
        try:
            for res_item in self.__travel_es(index=index, body=body):
                match_set |= set([m['_source']['api_id'] for m in res_item])
            return match_set
        except Exception as e:
            logger.info(e.__class__.__name__)