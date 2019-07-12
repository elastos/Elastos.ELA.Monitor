

# 检测程序搭建指南

## 依赖环境
- 安装python3、pip3、python3虚拟环境
- 安装mongodb
- 设置邮箱smtp

## 1. 软件安装

#### 1.1 安装python3.6及虚拟环境
    
1. 更新系统软件包并安装python3.6

```
$ sudo apt-get update
$ sudo apt-get install python3.6

# 如果出错：unable to locate package python3.6
执行：sudo add-apt-repository ppa:jonathonf/python-3.6

```
2. 安装pip3

```
sudo apt-get install python3-pip
```
3. 安装virtualenv

```
$ sudo apt-get install python-virtualenv

```
4. 创建python3虚拟环境

```
# 创建检测程序目录
$ mkdir ~/monitor
# 进入目录
$ cd ~/monitor
# 执行命令
$ virtualenv -p /usr/bin/python3 py3env

# 安装后有个py3env目录
```
    
#### 1.2 安装mongodb   

参考链接：https://www.aiuai.cn/aifarm671.html

1. 导入 MongoDB public GPG Key:

```
# 注意:整个命令是一行
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```
2. 创建 MongoDB 列表文件 list file - /etc/apt/sources.list.d/mongodb-org-4.0.list


```
# 注意:整个命令是一行
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/testing multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```

3. 安装 MongoDB

```
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org --force-yes
```

4. 启动服务

```
$ sudo service mongod start 

# 设置开机自动启动：
$ sudo systemctl enable mongod
```

## 2. 检测程序下载及设置

#### 2.1 下载程序

下载程序

```
# 拷贝Elastos.ELA.Monitor监测程序到服务器monitor
$ scp -r ./Elastos.ELA.Monitor username@ip:~/monitor

案例:
scp -r ./Elastos.ELA.Monitor root@192.168.2.123:~/monitor

# 查看监测程序是否已成功上传服务器
$ cd ～/monitor
$ ls 
#看到有Elastos.ELA.Monitor 说明上传程序已完成
```

#### 2.2 安装依赖包

```
# 进入python3虚拟环境
$ source ~/monitor/py3env/bin/activate
# 进入检测程序
$ cd ~/monitor/Elastos.ELA.Monitor
# 安装依赖包，如果报错，再执行一遍
$ pip3 install -r requirements.txt
```


#### 2.3 修改config文件ela参数
**ELA节点默认config文件未改的情况下只需添加node_publick_key参数**

```
# 查看运营公钥nodepublickey并添加公钥
1.进入默认节点目录下
$ cd ~/node/ela/

2. cli查看nodepublickey
$ ./ela-cli wallet a 或者 ./ela-cli wallet a -p 密码

例:
ADDRESS                            PUBLIC KEY                                                        
---------------------------------- ------------------------------------------------------------------
EJoF2mHeqgsmFU8psoDJ3TXPLw63xsNV5c 022a2cf2a38c40093650c567f1f4415d94d08170adcc9934f981aea8aca27ba9c3
---------------------------------- ------------------------------------------------------------------

3.复制public key 到python程序的config.py node_public_key
```

#### 2.4 设置smtp服务
**选择其中一种邮箱用来发送邮件**
**如果是阿里云和亚马逊服务器建议用Gmail邮箱**

1. 设置163邮箱smtp服务

参考链接:https://jingyan.baidu.com/article/7f41ecec3e8d35593d095c93.html

2. 设置qq邮箱smtp服务

参考链接:https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html
    
3. Gmail邮箱smtp服务默认开启，设置专用密码
参考链接:https://support.google.com/accounts/answer/185833#generate

#### 2.5 修改config.py的mail参数
1. 修改host

```
1.使用163邮箱
修改:
'host': 'smtp.163.com'
'port': 25

2.使用qq邮箱
修改：
'host': 'smtp.qq.com'
'port': 25

3.使用gmail邮箱
修改：
'host': 'smtp.gmail.com'
'port': 587
```


2. 修改user和pass

```
根据上面链接设置smtp的第三方登陆密码
user: 邮箱账号
pass: 第三方登陆密码(非邮箱账号登陆密码)
```

3. 修改sender邮件发送者

```
sender和user为同一个邮箱账号
```

4. 修改receivers邮件接受者

```
接受邮件可以是多个人,可以是任意格式邮箱,包括:gmil、163、qq
```

#### 2.6 设置定时任务

1. **第一次先执行程序**

```
# 执行检测程序，保证程序正常运行，收到邮件
# 进入shell目录
cd ~/monitor/Elastos.ELA.Monitor/shell/

# 执行顺序:
./add_onduty_info.sh ela 
./report_node.sh ela       
./report_onduty_info.sh ela
./report_peers.sh ela      
./warn_node_height.sh ela
./warn_onduty.sh ela       
./warn_onduty_viewoffset.sh ela    
./warn_producer_state.sh ela      
./warn_tx_pool.sh ela
```

2. 程序正常，设置定时任务

- 复制shell目录下的crontab.txt文件内容到crontab

1.进入crontab定时任务

```
$ crontab -e

    # Edit this file to introduce tasks to be run by cron.
    #
    # Each task to run has to be defined through a single line
    # indicating with different fields when the task will be run
    # and what command to run for the task
```

2.复制crontab.txt 到 crontab 最后一行

```
# 显示如下：
# m h  dom mon dow   command
00 01 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
00 11 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
```

3.退出crontab

```
$ ctrl + x
显示如下：
    Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES) ?
     Y Yes
     N No           ^C Cancel
```

4.输入 y 

5.输入enter

```
# 退出crontab后提示下面信息表示定时任务添加成功
crontab: installing new crontab
```

6.查看crontab定时任务是否成功添加

```
$ crontab -l
# 显示如下：
    00 01 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
    00 11 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
```

