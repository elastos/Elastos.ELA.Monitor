# Overview
- The purpose of this document is to first know the normal abnormal state of the arbitrator's node, and to send an early warning message if there are abnormal phenomena, and to deal with them correctly.

- To ensure that the arbitrator node can normally consensus on the block, it is necessary to know that the node can handle the abnormal situation quickly, so as to avoid unnecessary losses.

- Monitoring report sends mail at 9:00 a.m. and 7:00 p.m. every day, and early warning mail is sent in real time by nodes.

## 1.Monitor matters

#### 1.1 区块高度不同步预警

    The arbitrator node is highly inconsistent with other nodes, sending early warning mail to avoid the arbitrator not being able to identify the blocks normally and causing losses. It can observe whether the block height is synchronized by restarting the node and whether the Dpos direct connection network is normal (through the 1.8 direct connection reporting procedure). Block synchronization and direct connection status are normal, indicating that the arbitrator node is in normal operation.    
    
- 邮件格式

    时间 | 上次区块高度| 当前区块高度
    ---|---|---
    2019-06-07 02:45:37 | 359574| 359574


#### 1.2 节点RPC无法连接

    This arbitrator node RPC request timeout, or connection rejection, send early warning mail. The phenomenon may be that the server is unable to log on, the hard disk space is insufficient, and the nodes are at risk of hanging up. If one of these operations occurs, step 1.1 restores the node.

- 邮件格式

    时间 | 异常信息
    ---|---
    2019-06-14 22:24:53 | HTTPConnectionPool(host='127.0.0.1', port=20336): Max retries exceeded with url: / (Caused by NewConnectionError(': Failed to establish a new connection: [Errno 61] Connection refused',))


#### 1.3 视图切换预警

    This arbitrator Dpos consensus view switching too much, sending early warning mail. You can check whether the Dpos direct connection network is normal, and whether the node sends the proposal consensus block. If one of these operations occurs, step 1.1 restores the node.

    
- 邮件格式

    序号 | 区块高度| nodepublickey| 切换视图次数
    ---|---|---|---
    1 | 367731| 02e578a6f4295765ad3be4cdac9be15de5aedaf1ae76e86539bb54c397e467cd5e| 7

#### 1.4 连续不发送提案预警

    The arbitrator Dpos consensus does not send proposals continuously, and the arbitrator node can not normally consensus out blocks and send early warning mail. Manipulable Step 1.1 to Restore Nodes

- 邮件格式

    序号 | nodepublickey| 连续没有轮值区块高度范围
    ---|---|---
    2019-06-07 02:45:37 | 02e578a6f4295765ad3be4cdac9be15de5aedaf1ae76e86539bb54c397e467cd5e| 359550-359573

#### 1.5 状态预警

    The arbitrator Dpos consensus has abnormal phenomena and sends early warning mail. The inactave status indicates that the arbitrator has been excluded from the direct connection network and is not involved in the Dpos consensus block for the time being. The Dpos consensus of the arbitrator can be restored by sending an active transaction. Illegalegal state states: this arbitrator is guilty and can never participate in the Dpos consensus.
- 邮件格式

    nodepublickey| 仲裁人状态
    ---|---
    02e578a6f4295765ad3be4cdac9be15de5aedaf1ae76e86539bb54c397e467cd5e| inactive


#### 1.6 交易池遗留数据预警

    Part of the transaction still remains in the trading pool for three consecutive blocks. The arbitrator has not packaged the transaction for three consecutive blocks, stayed in the trading pool and sent early warning mail. Manipulable Step 1.1 to Restore Nodes

- 邮件格式

    区块高度| 遗留交易数
    ---|---
    359574 | 3
    
#### 1.7 区块高度报告

    Send the arbitrator's node height and the number of adjacent nodes regularly to understand that the node is in normal state.

- 邮件格式

    时间 | 区块高度| 相邻节点数
    ---|---|---
    2019-06-07 02:45:37 | 399728| 10


#### 1.8 Dpos直连报告

    Timely sending Dpos direct connection status information to understand that the arbitrator node can normally consensus on the block


- 邮件格式

    序号 | 区块高度| ownerpublickey| nodepublickey| 连接状态
    ---|---|---|---|---
    1 | 399728| *** 3633d3ddc8b ***| *** 0e3633d3ddc8b ***| 2WayConnection

#### 1.9 仲裁人报告信息

    Send the arbitrator's report information regularly to find out the number of consensus signatures, number of turn blocks and number of change views of the arbitrator's nodes.


- 邮件格式

    区块高度区间(343400-399732) | nodepublickey| 轮值次数| 签名次数|切换视图次数
    ---|---|---|---|---
    1 | *** ac9be15de5aedaf1ae76e86 *** | 4770| 47791| 1018