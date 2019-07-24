

# Guidelines for Build Monitor Procedures

## Dependent environment

- install python3、pip3、python3 virtualenv
- install mongodb
- set smtp

## 1. Install Software

#### 1.1 install python3.6 and python3 virtualenv
    
1. Update the system package and install python3.6

```
$ sudo apt-get update
$ sudo apt-get install python3.6

# If something goes wrong：unable to locate package python3.6
carry out order：sudo add-apt-repository ppa:jonathonf/python-3.6

```
2. Install pip3

```
sudo apt-get install python3-pip
```
3. Install virtualenv

```
$ sudo apt-get install python-virtualenv

```
4. Create python3 virtualenv

```
# create the monitor directory
$ mkdir ~/monitor
# enter directory
$ cd ~/monitor
# carry out order
$ virtualenv -p /usr/bin/python3 py3env

# There is a py3env directory after installation

```
    
#### 1.2 Install mongodb   

Reference link：https://www.aiuai.cn/aifarm671.html

1. Import MongoDB public GPG Key:

```
$ sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 9DA31620334BD75D9DCB49F368818C72E52529D4
```

2. Create MongoDB list file - /etc/apt/sources.list.d/mongodb-org-4.0.list

```
$ echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/testing multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-4.0.list
```

3. Install MongoDB

```
$ sudo apt-get update
$ sudo apt-get install -y mongodb-org --force-yes
```

4. Start server

```
$ sudo service mongod start 

# Set up boot-up auto-start：
$ sudo systemctl enable mongod
```

## 2. Elastos monitor download and setup

#### 2.1 Download 

```
# enter monitor 
$ cd ~/monitor
# wget download monitor
$ wget https://github.com/elastos/Elastos.ELA.Monitor/archive/master.zip
# unzip monitor
$ unzip master.zip
# rename
$ mv Elastos.ELA.Monitor-master Elastos.ELA.Monitor
```

#### 2.2 Install dependent environment

```
# enter python3 virtualenv
$ source ~/monitor/py3env/bin/activate
# enter elastos monitor
$ cd ~/monitor/Elastos.ELA.Monitor
# Install dependency packages and execute them again if an error is reported
$ pip3 install -r requirements.txt
```


#### 2.3 Modify the config configuration file ELA parameter

**If the default config file of ELA node is unchanged, only the node_publick_key parameter needs to be added**

```
# view nodepublickey and add publickey
1.Enter the ELA default node directory
$ cd ~/node/ela/

2. cli view nodepublickey
$ ./ela-cli wallet a or ./ela-cli wallet a -p password

eg:
ADDRESS                            PUBLIC KEY                                                        
---------------------------------- ------------------------------------------------------------------
EJoF2mHeqgsmFU8psoDJ3TXPLw63xsNV5c 022a2cf2a38c40093650c567f1f4415d94d08170adcc9934f981aea8aca27ba9c3
---------------------------------- ------------------------------------------------------------------

3.copy public key to config.py node_public_key of python program
```

#### 2.4 Set smtp server
**Select a mailbox to send mail**
**Recommend Gmail mailbox**

1. Set up 163 mailbox SMTP service

Reference link:https://jingyan.baidu.com/article/7f41ecec3e8d35593d095c93.html

2. Set up QQ mailbox SMTP service

Reference link:https://jingyan.baidu.com/article/6079ad0eb14aaa28fe86db5a.html
    
3. Gmail mailbox SMTP service opens by default and sets a private password

Reference link:https://support.google.com/accounts/answer/185833#generate

#### 2.5 Modify the mail parameters of config.py
1. Modify host

```
1.set up 163 mail server
modify:
'host': 'smtp.163.com'
'port': 25

2.set up qq mail server 
modify：
'host': 'smtp.qq.com'
'port': 25

3.set gmail mial server
modify：
'host': 'smtp.gmail.com'
'port': 587
```


2. Modify user and pass

```
Set the third party login password for SMTP according to the link above
user: Mail account
pass: Third party login password (non-mail account login password)
```

3. Modify mail sender

```
Sender and user are the same email account

```

4. Modify mail receivers

```
Receiving mail can be multiple people and can be in any format, including: gmil, 163, qq

```

#### 2.6 Set crontab

1. **First Execution Procedure**

```
# Execute the detection program to ensure the normal operation of the program and receive mail
# Enter the shell directory
cd ~/monitor/Elastos.ELA.Monitor/shell/

# Execution order:
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

2. Program is normal, set timed tasks

- Copy the contents of the crontab.txt file in the shell directory to crontab

1. Enter Crontab Timing Task

```
$ crontab -e

    # Edit this file to introduce tasks to be run by cron.
    #
    # Each task to run has to be defined through a single line
    # indicating with different fields when the task will be run
    # and what command to run for the task
```

2. Copy crontab. txt to the last line of crontab

```
File path：~/monitor/Elastos.ELA.Monitor/shell/crontab.txt
# It is shown below：
# m h  dom mon dow   command
00 01 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
00 11 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh
```

3. Exit crontab

```
$ ctrl + x
It is shown below：
    Save modified buffer (ANSWERING "No" WILL DESTROY CHANGES) ?
     Y Yes
     N No           ^C Cancel
```

4.Enter y 

5.Enter enter

```
# After exiting crontab, the following information is prompted to indicate that the timing task has been successfully added
crontab: installing new crontab
```

6.Check whether crontab timed tasks were successfully added

```
$ crontab -l
# It is shown below：
    00 01 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh ela
    00 11 * * *  ~/monitor/Elastos.ELA.Monitor/shell/report_node.sh ela
```

