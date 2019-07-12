# coding-UTF-8


import time

from common import node, rpc, email

'''
检测 mainnet 和 did 区块高度报告
'''

if __name__ == '__main__':
    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 28800))

    n = node.Node()

    b, height = rpc.getblockcount(n.url)
    assert b, 'getblockcount error:{}'.format(height)

    b, neighbors = rpc.getneighbors(n.url)
    assert b, 'getneighbors error:{}'.format(neighbors)

    mailText = "<tr><td width=" + str(80) + ">时间</td><td width=" + str(
        80) + ">区块高度</td><td width=" + str(80) + ">相邻节点数</td></tr>"

    mailText = mailText + "<tr><td>" + _time + "</td><td>" + str(
        height - 1) + "</td><td>" + str(len(neighbors)) + "</td></tr>"

    email.send_email(n.name + '报告信息', email.html_table(mailText))
    print('========== Test Finish ==========')
