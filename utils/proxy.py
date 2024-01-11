import requests

from config import PROXY_POOL_URL


def getProxy():
    ret = requests.get(PROXY_POOL_URL).json()
    proxy = {}
    if ret.get('proxy'):
        if ret['https']:
            proxy = {"https": {ret['proxy']}}
        else:
            proxy = {"http": {ret['proxy']}}
    return proxy
