#!/usr/bin/env python
# -*- coding:UTF-8 -*-


# DESCRIPTION: connect mongo


import pymongo
import config
# print(os.environ["PYTHONPATH"])


class MongoUtils:
    #连接数据库
    def __init__(self):
        client = pymongo.MongoClient("{}".format(config.mongo['host']))
        # print("{}".format(config.mongo['host']))
        #连接指定数据库
        self.db = client['course'] 

    def select(self, keywork:dict=None):
    # #指定goods 集合
        self.kwargs = keywork
        result = self.db['wx_message'].find(self.kwargs)
        # print(result) #<pymongo.cursor.Cursor object at 0x0000000002F3A7F0>
        for i in result: #需要遍历才能拿到每条document的信息
            print(i)


if __name__ == '__main__':
    test = MongoUtils()
    test.select({"msg_type":9999})
    