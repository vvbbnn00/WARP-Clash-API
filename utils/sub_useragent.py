
# common user agent for proxy application,
# format:
#   'user-agent' : 'app-name'
useragent_flag = {
    'clashforwindows': 'clash',
    'clashx': 'clash',
    'clashforandroid': 'clash',
    'clashmetaforandroid': 'meta',
    'clash-verge': 'meta',
    'clash.meta': 'meta',
    'surge': 'surge',
    'shadowrocket': 'shadowrocket',
    'v2ray': 'shadowrocket',
    'sing-box': 'sing-box',
    'loon': 'loon',
    'nekobox': 'nekobox',
}


def get_sub_type_from_ua(ua):
    for key in useragent_flag:
        if ua.find(key) != -1:
            return useragent_flag[key]
    # By default, return Clash
    return 'clash'