# coding=UTF-8

import pymongo
from common import interface


class OndutyMongoDBCont(object):
    ONDUTY_INFO = 'onduty_info'
    ONDUTY_HEIGHT = 'onduty_height'
    ONDUTY_VIEWOFFSET_HEIGHT = 'onduty_viewoffset_height'

    def __init__(self, mongo_host, mongo_port, mongo_db):
        self.client = ''
        self.db = ''
        self.getCon(mongo_host, mongo_port, mongo_db)

    '''获取连接'''

    def getCon(self, mongo_host, mongo_port, mongo_db):
        self.client = pymongo.MongoClient(mongo_host, mongo_port)  # 获取的连接
        self.db = self.client[mongo_db]  # 创建数据库db,默认detectorBlock
        self.add_index()

    '''添加索引'''

    def add_index(self):
        self.db[self.ONDUTY_INFO].ensure_index([(interface.height, 1)], unique=False)

    ''' 添加一条数据 '''

    def add_onduty_info(self, height, sponsor, view_offset, votes):
        try:
            self.db[self.ONDUTY_INFO].insert(
                {interface.height: height, interface.sponsor: sponsor, interface.view_offset: view_offset,
                 interface.votes: votes})
        except Exception as e:
            return e

    def add_onduty_height(self, height):
        try:
            self.db[self.ONDUTY_HEIGHT].insert(
                {interface.height: height})
        except Exception as e:
            return e

    def add_onduty_viewoffset_height(self, height):
        try:
            self.db[self.ONDUTY_VIEWOFFSET_HEIGHT].insert(
                {interface.height: height})
        except Exception as e:
            return e

    '''查询最后一条数据'''

    def findOne_onduty_info(self):
        try:
            content = self.db[self.ONDUTY_INFO].find().sort("_id", -1)
            for doc in content:
                return doc
        except Exception as e:
            return e

    def findOne_onduty_height(self):
        try:
            content = self.db[self.ONDUTY_HEIGHT].find().sort("_id", -1)
            for doc in content:
                return doc
        except Exception as e:
            return e

    def findOne_onduty_viewoffset_height(self):
        try:
            content = self.db[self.ONDUTY_VIEWOFFSET_HEIGHT].find().sort("_id", -1)
            for doc in content:
                return doc
        except Exception as e:
            return e

    def findOne_onduty_count(self):
        try:
            content = self.db[self.ONDUTY_INFO].find().count()
            return content
        except Exception as e:
            return e

    ''' 条件查询高度范围内的数据 '''

    def condition_find_onduty_sponsor(self, gte_height, lte_height):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$group': {'_id': '$' + interface.sponsor}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    ''' 视图内，仲裁人提案总次数 '''

    def condition_find_onduty_count(self, gte_height, lte_height):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$group': {'_id': '$' + interface.sponsor, 'count': {'$sum': 1}}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    ''' 视图内，切换视图总次数 '''

    def condition_find_viewoffset_count(self, gte_height, lte_height):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$group': {'_id': '$' + interface.sponsor, 'count': {'$sum': '$' + interface.view_offset}}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    ''' 视图内，仲裁人签名总次数 '''

    def condition_find_signer_count(self, gte_height, lte_height):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$unwind': '$' + interface.votes}, {'$group': {'_id': '$' + interface.votes, 'count': {'$sum': 1}}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    ''' 范围内，发送指定切换视图次数 '''

    def condition_find_viewoffset(self, gte_height, lte_height, number):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$match': {interface.view_offset: {'$gte': number}}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e

    ''' 范围内仲裁人不发提案，显示是否签名 '''

    def condition_find_signer(self, gte_height, lte_height, node_publickey):
        try:
            content = self.db[self.ONDUTY_INFO].aggregate(
                [{'$match': {interface.height: {'$gte': gte_height, '$lte': lte_height}}},
                 {'$unwind': '$' + interface.votes}, {'$match': {interface.votes: node_publickey}}])

            l = []
            for doc in content:
                l.append(doc)
            return l
        except Exception as e:
            return e
