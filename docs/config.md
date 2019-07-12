
```
ela = {'ip': '127.0.0.1',   // node server ip
       'http_json_port': 20336, // node rpc port number
       'mongo_db': 'block_ela', // mongo db name
       'mongo_host': '127.0.0.1', // mongo server ip
       'mongo_port': 27017, // mongo server port number
       'public_dpos_height': 402680, // the height start DPOS by CRCProducers and voted producers,default values
       'node_public_key': '02e578a6f4295765ad3be4cdac9be15de5aedaf1ae76e86539bb54c397e467cd5e', // operating public key
       "rpc_configuration": { // rpc authorization
              "user": '',
              "pass": ''
              }
       }

mail = {
       'host': 'smtp.163.com', // smtp server
       'port': 25, // smtp server port number 
       'user': 'elastos@163.com', // send mail user name
       'pass': 'elastos', // send mail password
       'sender': 'elastos@163.com', // send mail user name
       'receivers': ['elastos@163.com', 'elastos@qq.com', 'elastos@elastos.org'] // mail recipient
       }
       
```