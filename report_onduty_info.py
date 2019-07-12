# coding-UTF-8

from common import interface, node, email
from mongo import db_onduty_info
import add_onduty_info
import warn_onduty_viewoffset

''' 仲裁人轮值报告信息，切换视图报告、连续几轮不当值报告 '''
''' 当值仲裁人获取nickname 依赖与投票信息，所以先必须执行完投票信息才能执行此程序 '''


def onduty_report(n: node.Node, onduty_count, signer_count, viewoffset_count):
    onduty_map = dict()
    for i in range(len(onduty_count)):
        onduty = add_onduty_info.OndutyReport()
        node_publicKey = onduty_count[i].get('_id')
        if node_publicKey == n.node_public_key:
            onduty_map[node_publicKey] = onduty
            onduty.onduty_count = onduty_count[i].get('count')

    for i in range(len(signer_count)):
        if signer_count[i].get('_id') == n.node_public_key:
            onduty = onduty_map[signer_count[i].get('_id')]
            onduty.signer_count = signer_count[i].get('count')

    for i in range(len(viewoffset_count)):
        if viewoffset_count[i].get('_id') == n.node_public_key:
            onduty = onduty_map[viewoffset_count[i].get('_id')]
            onduty.viewoffset_count = viewoffset_count[i].get('count')

    print('=== onduty_map ==', onduty_map)
    return onduty_map


def onduty_info_mail(onduty_map: dict, gte_height, lte_height):
    ''' 仲裁人轮值报告 '''
    mail_text = "<tr><td width=" + str(200) + ">区块高度区间(" + str(gte_height) + "-" + str(
        lte_height) + ")</td><td width=" + str(
        100) + ">nodepublickey</td><td width=" + str(50) + ">轮值次数</td><td width=" + str(
        50) + ">签名次数</td><td width=" + str(50) + ">切换视图次数</td></tr>"
    num = 0
    key = onduty_map.keys()
    for node_publickey in key:
        onduty_value = onduty_map[node_publickey]
        onduty_count = onduty_value.onduty_count
        signer_count = onduty_value.signer_count
        viewoffset_count = onduty_value.viewoffset_count

        num += 1
        mail_text = mail_text + "<tr><td>" + str(num) + "</td><td>" + str(
            node_publickey) + "</td><td>" + str(onduty_count) + "</td><td>" + str(signer_count) + "</td><td>" + str(
            viewoffset_count) + "</td></tr>"

    return mail_text


if __name__ == '__main__':
    # 发送大于切换视图指定的数量
    number = 1

    n = node.Node()

    obj = db_onduty_info.OndutyMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)

    info = obj.findOne_onduty_info()
    onduty_height = obj.findOne_onduty_height()

    if info is None:
        assert False, 'db_onduty_info not data'

    db_height = info[interface.height]

    if onduty_height is not None:
        onduty_height = onduty_height[interface.height]
    else:
        onduty_height = n.public_dpos_height  # 默认主网H2设置高度

    # 区块范围内发送当值仲裁人的信息

    # 当值轮值次数
    onduty_count = obj.condition_find_onduty_count(onduty_height, db_height)
    # 签名次数
    signer_count = obj.condition_find_signer_count(onduty_height, db_height)
    # 切换视图次数
    viewoffset_count = obj.condition_find_viewoffset_count(onduty_height, db_height)

    print('onduty_count :  ', onduty_count)
    print('signer_count :  ', signer_count)
    print('viewoffset_count :  ', viewoffset_count)

    # 发送报告

    onduty_map = onduty_report(n, onduty_count, signer_count, viewoffset_count)
    on_mail = onduty_info_mail(onduty_map, onduty_height, db_height)

    v_mail = warn_onduty_viewoffset.onduty_viewoffset(obj, n, onduty_height, db_height, number)

    # print("=======send :", send_email.html_table(on_mail) + send_email.html_table(v_mail))
    email.send_email(n.name + '仲裁人报告信息', email.html_table(on_mail) + email.html_table(v_mail))

    obj.add_onduty_height(db_height)
    print('========== Test Finish ==========')
