import requests

from config import PROXY_POOL_URL


def getProxy():
    """
    Get proxy from proxy pool
    :return: proxy got from proxy pool
    """
    ret = requests.get(PROXY_POOL_URL).json()
    proxy = {}
    if ret.get('proxy'):
        if ret['https']:
            proxy = {"https": {ret['proxy']}}
        else:
            proxy = {"http": {ret['proxy']}}
    return proxy
