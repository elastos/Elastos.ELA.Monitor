# coding-UTF-8
from common import rpc, node, interface, email
from mongo import db_tx_pool


def txid(result):
    txs = set()
    for i in range(len(result)):
        r = result[i]
        txs.add(r[interface.txid])
    return txs


if __name__ == '__main__':
    n = node.Node()
    b, result = rpc.getrawmempool(n.url)
    assert b, 'getrawmempool error:{}'.format(result)

    obj = db_tx_pool.TxPoolMongoDBCont(n.mongo_host, n.mongo_port, n.mongo_db)
    b, height = rpc.getblockcount(n.url)
    assert b, '[warn_node_height.py] getblockcount error:{}'.format(height)

    if result is not None:
        txids = txid(result)
        db_txs = obj.find_tx_pool()
        if db_txs is not None:
            db_tx = obj.findOne_tx_pool()
            # db count > 3
            if len(db_txs) > 2 and db_tx[interface.height] > height - 1:
                tx_pool = db_txs[0]
                tx_pool_1 = db_txs[1]
                tx_pool_2 = db_txs[2]

                tx_1 = tx_pool.intersection(tx_pool_1)
                tx_2 = tx_1.intersection(tx_pool_2)
                if len(tx_2) == 0:
                    obj.drop_tx_pool()
                else:
                    obj.drop_tx_pool()
                    mail_text = "<tr><td width=" + str(
                        100) + ">区块高度</td><td width=" + str(100) + ">遗留交易数</td></tr>"

                    mail_text = mail_text + "<tr><td>" + str(height - 1) + "</td><td>" + str(len(tx_2)) + "</td></tr>"
                    email.send_email(n.name + '交易池遗留交易预警', email.html_table(mail_text))
            else:
                obj.add_tx_pool(height - 1, txids)
        else:
            obj.add_tx_pool(height - 1, txids)

    else:
        obj.drop_tx_pool()
    print('========== Test Finish ==========')
