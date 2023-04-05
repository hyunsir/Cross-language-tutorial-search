# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-----------------------------------------
@Author: gaoya
@Email: 21212010053@m.fudan.edu.cn
@Created: 2022/11/21
------------------------------------------
@Modify: 2022/11/21
------------------------------------------
@Description:
"""
from milvus import Milvus
from util.file_util import FileUtil
from util.path_util import PathUtil


class MilvusUtil:
    milvus_config_path = PathUtil.milvus_config_path()
    milvus_list = FileUtil.load_data_list(milvus_config_path)
    milvus_config = milvus_list[0]

    def delete(self, index):
        mi = Milvus(host=self.milvus_config['host'], port=self.milvus_config['port'])
        re = mi.drop_collection(index)
        return re
