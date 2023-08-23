import requests


def getProxy():
    ret = requests.get("https://getproxy.bzpl.tech/get/").json()
    proxy = {}
    if ret.get('proxy'):
        if ret['https']:
            proxy = {"https": {ret['proxy']}}
        else:
            proxy = {"http": {ret['proxy']}}
    return proxy

