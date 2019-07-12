# coding-UTF-8

from common import email, rpc, node

''' 发送当前仲裁人直连信息 '''

if __name__ == '__main__':

    n = node.Node()

    b, height = rpc.getblockcount(n.url)
    assert b, 'getblockcount error:{}'.format(height)

    b, arbiters = rpc.getarbiterpeersinfo(n.url, height - 1)
    assert b, 'getarbiterpeersinfo error:{}'.format(arbiters)

    # print('arbiters :', arbiters)
    mailText = "<tr><td width=" + str(20) + ">序号</td><td width=" + str(20) + ">区块高度</td><td width=" + str(
        200) + ">ownerpublickey</td><td width=" + str(200) + ">nodepublickey</td><td width=" + str(20) + ">连接状态</td></tr>"

    print('arbiterpeersinfo:', arbiters)
    for i in range(len(arbiters)):
        arbiter = arbiters[i]
        owner_public_key = arbiter['ownerpublickey']
        node_public_key = arbiter['nodepublickey']
        state = arbiter['connstate']

        mailText = mailText + "<tr><td>" + str(i + 1) + "</td><td>" + str(
            height - 1) + "</td><td>" + owner_public_key + "</td><td>" + node_public_key + "</td><td>" + state + "</td></tr>"
        print('teest :', mailText)

    email.send_email(n.name + '仲裁人直连报告', email.html_table(mailText))
