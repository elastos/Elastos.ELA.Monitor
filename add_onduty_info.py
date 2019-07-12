# coding=UTF-8

from common import rpc, node, interface
from mongo import db_onduty_info

"""
@author: DongLei.Tan
@license: Apache Licence 
@contact: tandonglei28@gmail.com
@file: add_onduty_info.py
@time: 2019/04/16
"""

''' 当值仲裁人信息实时写入数据库 '''


class OndutyReport(object):
    def __init__(self):
        self.nickname = ''
        self.height = 0
        self.onduty_count = 0
        self.signer_count = 0
        self.viewoffset_count = 0


if __name__ == '__main__':
    n = node.Node()

    obj = db_onduty_info.OndutyMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)

    b, height = rpc.getblockcount(n.url)
    assert b, '[add_onduty_info] get_block_count : '.format(height)

    info = obj.findOne_onduty_info()
    db_height = ''
    if info is None:
        db_height = n.public_dpos_height  # 默认主网H2设置高度
    else:
        db_height = info[interface.height] + 1

    # 遍历区块高度保存当值仲裁人信息
    for h in range(db_height, height):
        print('============================= height: {} ============================='.format(h))
        b, result = rpc.getconfirmbyheight(n.url, h)
        assert b, '[add_onduty_info] get_confirm_by_height : '.format(height)
        sponsor = result['sponsor']
        view_offset = result['viewoffset']
        votes = result['votes']
        signers = []
        for v in range(len(votes)):
            signer = votes[v].get('signer')
            signers.append(signer)
        print('signers = ', signers)
        obj.add_onduty_info(h, sponsor, view_offset, signers)
