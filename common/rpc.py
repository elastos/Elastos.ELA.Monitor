# coding=UTF-8

import requests
import config
from requests.auth import HTTPDigestAuth

rpc_user = ''
rpc_pass = ''

''' 通过地址获取 utxo  '''


def listunspent(url, addresses):
    resp = post_request(url, "listunspent", params={"addresses": addresses})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 根据txid 获取交易信息 '''


def getrawtransaction(url, txid, verbose=True):
    resp = post_request(url, "getrawtransaction", params={"txid": txid, "verbose": verbose})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 获取当前区块高度 '''


def getblockcount(url):
    resp = post_request(url, "getblockcount", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 通过height获取区块hash '''


def getblockhash(url, height):
    resp = post_request(url, "getblockhash", params={"height": height})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 通过height获取区块hash '''


def getblockhash_(url, height):
    resp = post_request(url, "getblockhash", params={"height": str(height)})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 通过区块hash获取区块信息 '''


def getblock(url, blockhash, verbosity=2):
    resp = post_request(url, "getblock", params={"blockhash": blockhash, "verbosity": verbosity})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 通过区块Height获取区块信息 '''


def getblockbyheight(url, height):
    resp = post_request(url, "getblockbyheight", params={"height": height})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' 获取邻居节点信息 '''


def getneighbors(url):
    resp = post_request(url, "getneighbors", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


''' arbiter服务器侧链 '''


def getmainchainblockheight(url):
    resp = post_request(url, "getmainchainblockheight", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getsidechainblockheight(url, hash):
    resp = post_request(url, "getsidechainblockheight", params={"hash": hash})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def listproducers(url, state=None):
    if state is None:
        resp = post_request(url, "listproducers", params={})
    else:
        resp = post_request(url, "listproducers", params={"state": state})

    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getspvheight(url):
    resp = post_request(url, "getspvheight", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getarbiterpeersinfo(url, height):
    resp = post_request(url, "getarbiterpeersinfo", params={"height": height})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getconfirmbyheight(url, height):
    resp = post_request(url, "getconfirmbyheight", params={"height": height, "verbosity": 1})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getarbitersinfo(url):
    resp = post_request(url, "getarbitersinfo", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def getrawmempool(url):
    resp = post_request(url, "getrawmempool", params={})
    if resp["error"] is None:
        return True, resp["result"]
    else:
        return False, resp["error"]


def post_request(url, method, params={}):
    try:
        resp = requests.post(url, json={"method": method, "params": params},
                             headers={"content-type": "application/json"}, timeout=60,
                             auth=requests.auth.HTTPBasicAuth(rpc_user, rpc_pass))
        return resp.json()
    except requests.exceptions.RequestException as e:
        # print("Post Requiest Error:", e)
        return {'error': e}
