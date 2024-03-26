"""

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, see <https://www.gnu.org/licenses>.

"""

# common user agent for proxy application,
# format:
#   'user-agent': 'app-name'
USERAGENT_FLAG = {
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


def getSubTypeFromUA(ua):
    """
    Get subscription type from useragent
    :param ua: useragent
    :return:
    """
    for key in USERAGENT_FLAG:
        if ua.find(key) != -1:
            return USERAGENT_FLAG[key]
    # By default, return Clash
    return 'clash'
