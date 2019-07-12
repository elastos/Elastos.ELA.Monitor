# coding-UTF-8
import pymongo
from common import interface


class TxPoolMongoDBCont(object):
    TX_POOL = 'tx_pool'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.client = ''
        self.db = ''
        self.getCon(mongo_host, mongo_port, mongo_db)

    '''获取连接'''

    def getCon(self, mongo_host, mongo_port, mongo_db):
        self.client = pymongo.MongoClient(mongo_host, mongo_port)  # 获取的连接
        self.db = self.client[mongo_db]  # 创建数据库db,默认detectorBlock

    ''' 添加一条数据 '''

    def add_tx_pool(self, height, tx_pool):
        try:
            self.db[self.TX_POOL].insert({interface.height: height, interface.tx_pool: tx_pool})
        except Exception as e:
            return e

    '''查询最后一条数据'''

    def findOne_tx_pool(self):
        try:
            content = self.db[self.TX_POOL].find().sort("_id", -1)
            for doc in content:
                return doc
        except Exception as e:
            return e

    def find_tx_pool(self):
        try:
            content = self.db[self.TX_POOL].find()
            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    def delete_tx_pool(self, height):
        try:
            content = self.db[self.TX_POOL].delete_one({interface.height: height})
            for doc in content:
                return doc
        except Exception as e:
            return e

    def drop_tx_pool(self):
        try:
            content = self.db[self.TX_POOL].drop()
            for doc in content:
                return doc
        except Exception as e:
            return e
