# coding-UTF-8
import pymongo
from common import interface


class DetectorMongoDBCont(object):
    HEIGHT_DISCRETE = 'height_discrete'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.client = ''
        self.db = ''
        self.getCon(mongo_host, mongo_port, mongo_db)

    '''获取连接'''

    def getCon(self, mongo_host, mongo_port, mongo_db):
        self.client = pymongo.MongoClient(mongo_host, mongo_port)  # 获取的连接
        self.db = self.client[mongo_db]  # 创建数据库db,默认detectorBlock

    ''' 添加一条数据 '''

    def add_discrete_height(self, height):
        try:
            self.db[self.HEIGHT_DISCRETE].insert({interface.height: height})
        except Exception as e:
            return e

    '''查询最后一条数据'''

    def findOne_discreteHeight(self):
        try:
            content = self.db[self.HEIGHT_DISCRETE].find().sort("_id", -1)
            for doc in content:
                return doc
        except Exception as e:
            return e
