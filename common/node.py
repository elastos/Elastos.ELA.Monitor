import argparse

import config
from common import rpc


class Node(object):
    def __init__(self):
        self.activate_net = 'ela'
        self.ip = ''
        self.name = ''
        self.port = 0
        self.url = ''
        self.mongo_host = ''
        self.mongo_port = 0
        self.mongo_db = ''
        self.public_dpos_height = 0
        self.node_public_key = 0
        self._init_config()

    def _init_config(self):
        self.get_activate_net()
        if self.activate_net == 'ela':
            self.port = config.ela['http_json_port']
            self.ip = config.ela['ip']
            self.name = '[ELA]'
            self.mongo_host = config.ela['mongo_host']
            self.mongo_port = config.ela['mongo_port']
            self.mongo_db = config.ela['mongo_db']
            self.public_dpos_height = config.ela['public_dpos_height']
            self.node_public_key = config.ela['node_public_key']
            self.get_url()
            self.get_rpc_auth()

    def get_activate_net(self):
        parser = argparse.ArgumentParser(description="input parameter")
        parser.add_argument('-n', '--net', type=str, dest='net', help='node type')
        args = parser.parse_args()
        if args.net:
            self.activate_net = args.net

    def get_url(self):
        self.url = 'http://' + self.ip + ':' + str(self.port)

    def get_rpc_auth(self):
        try:
            if self.activate_net == 'ela':
                rpc_configuration = config.ela['rpc_configuration']
                rpc.rpc_user = rpc_configuration.get('user')
                rpc.rpc_pass = rpc_configuration.get('pass')
        except Exception as e:
            print('get_rpc_auth, error:{}'.format(e))
