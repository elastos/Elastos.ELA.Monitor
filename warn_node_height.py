
import time

from common import node, rpc, email
from mongo import db_height_discrete

if __name__ == '__main__':

    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 28800))

    n = node.Node()

    b, height = rpc.getblockcount(n.url)
    if b is False:
        email.send_email(n.name + '异常报告', email.html_table(
            "<tr><td width=" + str(20) + ">时间</td><td width=" + str(200) + ">异常信息</td></tr><tr><td>" + str(_time) + "</td><td>" + str(height) + "</td></tr>"))

    assert b, '[warn_node_height.py] getblockcount error:{}'.format(height)

    obj = db_height_discrete.DetectorMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)

    ''' detection of block height growth '''
    print('======= detection of block height growth  ========')
    discreteHeight = obj.findOne_discreteHeight()
    print('discreteHeight:{},basicHeight:{}'.format(discreteHeight, height))
    if discreteHeight is None:
        obj.add_discrete_height(height)

    elif discreteHeight['height'] == height:
        mail_text = "<tr><td width=" + str(20) + ">时间</td><td width=" + str(80) + ">上次区块高度</td><td width=" + str(
            80) + ">当前区块高度</td></tr>"
        mail_text = mail_text + "<tr><td>" + str(_time) + "</td><td>" + str(
            discreteHeight['height']) + "</td><td>" + str(
            height) + "</td></tr>"
        email.send_email(n.name + '区块高度不增长', email.html_table(email.html_table(mail_text)))

    elif discreteHeight['height'] < height:
        obj.add_discrete_height(height)
    print('========== Test Finish ==========')
