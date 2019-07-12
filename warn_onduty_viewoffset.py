# coding-UTF-8


from common import interface, node, email
from mongo import db_onduty_info
import add_onduty_info


def viewoffset_report(n: node.Node, viewoffset_info):
    view_list = list()

    for i in range(len(viewoffset_info)):
        view_map = dict()
        onduty = add_onduty_info.OndutyReport()
        nodepublickey = viewoffset_info[i].get(interface.sponsor)

        if nodepublickey == n.node_public_key:
            view_map[nodepublickey] = onduty
            onduty.height = viewoffset_info[i].get(interface.height)
            onduty.viewoffset_count = viewoffset_info[i].get(interface.view_offset)
            view_list.append(view_map)

    print('=== view_list ==', len(view_list))
    return view_list


def _viewoffset_mail(view_list: list):
    ''' 大于指定视图切换次数的仲裁人信息 '''

    mail_text = "<tr><td width=" + str(20) + ">序号</td><td width=" + str(200) + ">区块高度</td><td width=" + str(
        100) + ">nodepublickey</td><td width=" + str(50) + ">切换视图次数</td></tr>"
    num = 0
    for i in range(len(view_list)):
        view_map = view_list[i]
        for node_publickey in view_map.keys():
            onduty_value = view_map[node_publickey]
            height = onduty_value.height
            viewoffset = onduty_value.viewoffset_count

            num += 1
            mail_text = mail_text + "<tr><td>" + str(num) + "</td><td>" + str(height) + "</td><td>" + str(
                node_publickey) + "</td><td>" + str(viewoffset) + "</td></tr>"

    return mail_text


''' 该方法可做预警可做报告 '''


def onduty_viewoffset(obj, n: node.Node, db_height: int, height: int, number: int):
    # 大于指定视图次数仲裁人信息
    viewoffset_info = obj.condition_find_viewoffset(db_height, height, number)
    print('viewoffset_info :  ', len(viewoffset_info))

    v_mail = ''
    if len(viewoffset_info) != 0:
        view_list = viewoffset_report(n, viewoffset_info)
        if len(view_list) > 0:
            v_mail = _viewoffset_mail(view_list)
    return v_mail


if __name__ == '__main__':
    # 发送大于切换视图指定的数量
    number = 2

    n = node.Node()

    obj = db_onduty_info.OndutyMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)

    info = obj.findOne_onduty_info()
    viewoffset_height = obj.findOne_onduty_viewoffset_height()
    db_height = ''
    if info is not None:
        db_height = info[interface.height]
    else:
        assert False, '[warn_onduty_viewoffset.py] mongodb not onduty_info'

    if viewoffset_height is not None:
        viewoffset_height = viewoffset_height[interface.height]
    else:
        viewoffset_height = n.public_dpos_height  # 默认主网H2设置高度

    v_mail = onduty_viewoffset(obj, n, viewoffset_height, db_height, number)
    if v_mail != '':
        email.send_email(n.name + '仲裁人切换视图预警', email.html_table(v_mail))
        obj.add_onduty_viewoffset_height(db_height)
    print('========== Test Finish ==========')
