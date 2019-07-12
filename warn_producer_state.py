# coding-UTF-8
import time

from common import node, rpc, interface, email

if __name__ == '__main__':
    _time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time() + 28800))

    n = node.Node()

    mailText = ''

    b, result = rpc.listproducers(n.url, state=interface.inactive)
    producers = result[interface.producers]
    if producers is not None:
        for i in range(len(producers)):
            proudcer = producers[i]
            if proudcer[interface.node_publicKey] == n.node_public_key:
                mailText = mailText + "<tr><td>" + n.node_public_key + "</td><td>" + interface.inactive + "</td></tr>"

    b, result = rpc.listproducers(n.url, state=interface.illegal)
    assert b, 'listproducers error:{}'.format(result)
    producers = result[interface.producers]
    if producers is not None:
        for i in range(len(producers)):
            proudcer = producers[i]
            if proudcer[interface.node_publicKey] == n.node_public_key:
                mailText = mailText + "<tr><td>" + n.node_public_key + "</td><td>" + interface.illegal + "</td></tr>"

    print('email.html_table(mail + mailText):', mailText)
    if mailText != '':
        mail = "<tr><td width=" + str(80) + ">nodepublickey</td><td width=" + str(80) + ">仲裁人状态</td></tr>"
        email.send_email(n.name + '仲裁人状态预警', '[' + str(_time) + ']' + email.html_table(mail + mailText))
    print('========== Test Finish ==========')
