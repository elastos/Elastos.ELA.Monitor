# coding-UTF-8

from common import email

from common import node, interface
from mongo import db_onduty_info

''' 当值仲裁人连续没有出块预警 '''


def _get_vote(obj, node_public_key, gte_height_2: int, height: int):
    mail_text = "<tr><td width=" + str(20) + ">序号</td><td width=" + str(
        100) + ">nodepublickey</td><td width=" + str(100) + ">签名高度</td></tr>"

    num = 0
    votes = obj.condition_find_signer(gte_height_2, height, node_public_key)
    print('==== votes :', votes)
    if len(votes) != 0:
        for i in range(len(votes)):
            vote = votes[i]
            height = vote.get('height')
            num += 1
            mail_text = mail_text + "<tr><td>" + str(num) + "</td><td>" + node_public_key + "</td><td>" + str(
                height) + "</td></tr>"
    return mail_text


def _onduty_mail(node_public_key, gte_height_2: int, height: int):
    mail_text = "<tr><td width=" + str(20) + ">序号</td><td width=" + str(
        100) + ">nodepublickey</td><td width=" + str(100) + ">连续没有轮值区块高度范围</td></tr>"

    mail_text = mail_text + "<tr><td>" + str(0) + "</td><td>" + node_public_key + "</td><td>" + str(
        gte_height_2) + "-" + str(height) + "</td></tr>"
    return mail_text


if __name__ == '__main__':
    arbiter_num = 36

    n = node.Node()
    node_public_key = n.node_public_key

    ''' connect to the database to get the latest height and total data '''
    obj = db_onduty_info.OndutyMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)
    onduty = obj.findOne_onduty_info()
    # print('onduty : ', onduty)

    height = onduty.get(interface.height)

    onduty_count = obj.findOne_onduty_count()
    # print('onduty_count : ', onduty_count)

    ''' 连续两次当值仲裁人不出块逻辑, 判断数据库数据是否大于24个 '''
    if onduty_count >= arbiter_num * 2:

        gte_height_1 = height - arbiter_num + 1
        gte_height_2 = height - arbiter_num * 2 + 1

        print('block height :{},{}'.format(gte_height_1, height))
        onduty = obj.condition_find_onduty_sponsor(height - arbiter_num + 1, height)
        m_sponsor = set()
        for i in range(len(onduty)):
            sponsor = onduty[i].get('_id')
            m_sponsor.add(sponsor)
        print('m_sponsor_1 : ', m_sponsor)

        if node_public_key in m_sponsor:
            assert False, '[normal] First round send the proposal, close the process'

        print('block height :{},{}'.format(gte_height_2, gte_height_1 - 1))
        onduty = obj.condition_find_onduty_sponsor(gte_height_2, height - arbiter_num)
        m_sponsor = set()
        for i in range(len(onduty)):
            sponsor = onduty[i].get('_id')
            m_sponsor.add(sponsor)
        print('m_sponsor_2 : ', m_sponsor)

        if node_public_key in m_sponsor:
            assert False, '[normal] Second round send the proposal, close the process'

        ''' 最后的两个集合的sponsor一致，发送邮件 '''
        mail = _onduty_mail(node_public_key, gte_height_2, height)

        mail_vote = _get_vote(obj, node_public_key, gte_height_2, height)

        email.send_email(n.name + '连续不发送提案预警',
                         email.html_table(mail) + email.html_table(mail_vote))

    print('========== Test Finish ==========')
