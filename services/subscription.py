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
import base64
import configparser
import copy
import json
import logging
import random
import string
import tempfile
import urllib.parse

import yaml
from flask import request

from config import PUBLIC_URL, RANDOM_COUNT, SECRET_KEY, SHARE_SUBSCRIPTION
from models import Account
from services.common import getCurrentAccount
from utils.entrypoints import getEntrypoints, getBestEntrypoints
from utils.geoip import GeoIP
from utils.node_name import NodeNameGenerator

CF_CONFIG = json.load(open("./config/cf-config.json", "r", encoding="utf8"))
CLASH = json.load(open("./config/clash.json", "r", encoding="utf8"))

SURGE = configparser.ConfigParser()
SURGE.read("./config/surge.conf", encoding="utf8")
SURGE_RULE = open("./config/surge-rule.txt", "r", encoding="utf8").read()
SURGE_SUB = open("./config/surge-sub.txt", "r", encoding="utf8").read()

SING_BOX = json.load(open("./config/sing-box.json", "r", encoding="utf8"))

GEOIP = GeoIP('./config/geolite/GeoLite2-Country.mmdb')


def getRandomEntryPoints(best=False,
                         logger=logging.getLogger(__name__),
                         ipv6=False):
    """
    Get random entry points
    :param best: Whether to use the best entrypoints
    :param logger:
    :param ipv6: Whether to use ipv6 entrypoints
    :return: list of entrypoints
    """
    entrypoints = getEntrypoints(ipv6=ipv6)

    # If there is no entrypoints, return a message
    if entrypoints is None or len(entrypoints) == 0:
        return None, "No entrypoints available. Please try again later."

    # Randomly select entrypoints
    if len(entrypoints) < RANDOM_COUNT:
        logger.warning(f"Entrypoints is less than {RANDOM_COUNT}, only {len(entrypoints)} available.")
        random_points = entrypoints
    else:
        random_points = random.sample(entrypoints, RANDOM_COUNT) if not best else getBestEntrypoints(RANDOM_COUNT,
                                                                                                     ipv6=ipv6)

    return random_points, ""


def generateClashSubFile(account: Account = None,
                         logger=logging.getLogger(__name__),
                         best=False,
                         proxy_format='full',
                         random_name=False,
                         is_android=False,
                         ipv6=False):
    """
    Generate Clash subscription file
    :param random_name: Whether to use random name
    :param proxy_format: full - full config, with_groups - only proxies and proxy-groups, only_proxies - only proxies
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :param is_android: Whether the client is Android
    :param ipv6: Whether to use ipv6 entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account

    random_points, msg = getRandomEntryPoints(best, logger, ipv6=ipv6)
    if random_points is None:
        return msg

    # Generate user configuration file
    user_config = []

    # Initialize NodeNameGenerator
    node_name_generator = NodeNameGenerator(random_name)

    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        country = GEOIP.lookup(point.ip)
        country_emoji = GEOIP.lookup_emoji(point.ip)
        name = node_name_generator.next(country_emoji, country)
        config_data = {
            "name": name,
            "type": "wireguard",
            "server": point.ip,
            "port": point.port,
            "ip": "172.16.0.2",
            "private-key": account.private_key,
            "public-key": CF_CONFIG.get("publicKey"),
            "udp": True,
            "remote-dns-resolve": True,
            "mtu": 1280,
        }

        # It seems that `dns` will cause problem in android.
        if not is_android:
            config_data["dns"] = ['1.1.1.1', '1.0.0.1']

        user_config.append(config_data)
    clash_json = copy.deepcopy(CLASH)
    clash_json["proxies"] = user_config
    for proxy_group in clash_json["proxy-groups"]:
        proxy_group["proxies"] += [proxy["name"] for proxy in user_config]

    # Generate YAML file
    if proxy_format == 'only_proxies':
        clash_yaml = yaml.dump({'proxies': clash_json['proxies']},
                               allow_unicode=True)
    elif proxy_format == 'with_groups':
        clash_yaml = yaml.dump({'proxies': clash_json['proxies'],
                                'proxy-groups': clash_json['proxy-groups']},
                               allow_unicode=True)
    else:
        clash_yaml = yaml.dump(clash_json, allow_unicode=True)
    return clash_yaml


def generateWireguardSubFile(account: Account = None,
                             logger=logging.getLogger(__name__),
                             best=False,
                             ipv6=False):
    """
    Generate Wireguard subscription file
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :param ipv6: Whether to use ipv6 entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = getEntrypoints(ipv6=ipv6)

    # If there is no entrypoints, return a message
    if entrypoints is None or len(entrypoints) == 0:
        return "No entrypoints available. Please try again later."

    random_point = random.choice(entrypoints) if not best else getBestEntrypoints(1, ipv6=ipv6)[0]

    ip = random_point.ip
    if ipv6:
        ip = f"[{ip}]"  # ipv6 address should be wrapped in square brackets

    # Generate user configuration file
    text = f"""[Interface]
PrivateKey = {account.private_key}
Address = 172.16.0.2/32
DNS = 1.1.1.1
MTU = 1280

[Peer]
PublicKey = {CF_CONFIG.get("publicKey")}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {ip}:{random_point.port}
PersistentKeepalive = 25
"""
    return text


def generateSurgeSubFile(account: Account = None,
                         logger=logging.getLogger(__name__),
                         best=False,
                         proxy_format='full',
                         random_name=False,
                         ipv6=False):
    """
    Generate Surge subscription file
    :param random_name: Whether to use random name
    :param proxy_format: full - full config, with_groups - only proxies and proxy-groups, only_proxies - only proxies
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :param ipv6: Whether to use ipv6 entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account

    random_points, msg = getRandomEntryPoints(best, logger, ipv6)
    if random_points is None:
        return msg

    # Generate user configuration file
    user_config = []

    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        ip = point.ip
        if ipv6:
            ip = f"[{ip}]"  # ipv6 address should be wrapped in square brackets
        user_config.append(
            {
                "self-ip": "172.16.0.2",
                "private-key": account.private_key,
                "dns-server": "1.1.1.1",
                "mtu": 1420,
                "peer": f'(public-key = {CF_CONFIG.get("publicKey")}, allowed-ips = "0.0.0.0/0, ::/0", '
                        f'endpoint = {ip}:{point.port})',
                "endpoint": f"{ip}|{point.port}"
            })

    surge_config = copy.deepcopy(SURGE)

    # Initialize NodeNameGenerator
    node_name_generator = NodeNameGenerator(random_name)

    for config in user_config:
        # random a name like 2FDEC93F, num and upper letter
        name = ''.join(random.sample(string.ascii_uppercase + string.digits, 8))

        ip = config['endpoint'].split("|")[0]
        country = GEOIP.lookup(ip)
        country_emoji = GEOIP.lookup_emoji(ip)
        del config['endpoint']

        proxy_name = node_name_generator.next(country_emoji, country)

        surge_config[f'WireGuard {name}'] = config
        surge_config['Proxy'][proxy_name] = f'wireguard, section-name={name}'

    surge_config['Proxy Group']['proxy'] = f"select, auto, fallback, {', '.join(surge_config['Proxy'].keys())}"
    surge_config['Proxy Group']['auto'] = (f"url-test, {', '.join(surge_config['Proxy'].keys())}, "
                                           f"url=http://www.gstatic.com/generate_204, interval=43200")
    surge_config['Proxy Group']['fallback'] = (f"fallback, {', '.join(surge_config['Proxy'].keys())}, "
                                               f"url=http://www.gstatic.com/generate_204, interval=43200")

    # generate a tmp file to store the path of surge.ini
    temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False, encoding='utf8')
    surge_config.write(temp_file)
    temp_file.seek(0)
    surge_ini = temp_file.read()

    # Generate INI file
    if proxy_format == 'with_groups' or proxy_format == 'only_proxies':
        pass
    else:
        surge_ini += SURGE_RULE

    # Generate subscription link, use public_url if it is not None
    public_url = PUBLIC_URL
    if public_url is None:
        # Get public url from request
        public_url = request.url_root[:-1]

    public_url = f"{public_url}/api/surge?best={str(best).lower()}&randomName={str(random_name).lower()}"
    if SECRET_KEY is not None and SHARE_SUBSCRIPTION is False:
        public_url += f"&key={SECRET_KEY}"

    surge_ini = SURGE_SUB.replace("{PUBLIC_URL}", public_url) + surge_ini

    return surge_ini


def generateShadowRocketSubFile(account: Account = None,
                                logger=logging.getLogger(__name__),
                                best=False,
                                random_name=False,
                                ipv6=False):
    """
    Generate ShadowRocket subscription file
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :param random_name: Whether to use random name
    :param ipv6: Whether to use ipv6 entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account

    random_points, msg = getRandomEntryPoints(best, logger, ipv6)
    if random_points is None:
        return msg

    # Initialize NodeNameGenerator
    node_name_generator = NodeNameGenerator(random_name)

    url_list = []
    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        country = GEOIP.lookup(point.ip)
        country_emoji = GEOIP.lookup_emoji(point.ip)
        name = node_name_generator.next(country_emoji, country)
        ip = point.ip
        if ipv6:
            ip = f"[{ip}]"  # ipv6 address should be wrapped in square brackets
        url = f"wg://{ip}:{point.port}?publicKey={CF_CONFIG.get('publicKey')}&privateKey={account.private_key}" \
              f"&dns=1.1.1.1,1.0.0.1" \
              f"&ip=172.16.0.2&udp=1&flag={country}#{urllib.parse.quote(name)}"
        url_list.append(url)

    sub_data = "\n".join(url_list)
    sub_data = base64.b64encode(sub_data.encode("utf-8")).decode("utf-8")

    return sub_data


def generateSingBoxSubFile(account: Account = None,
                           logger=logging.getLogger(__name__),
                           random_name=False,
                           best=False,
                           ipv6=False):
    """
    Generate SingBox subscription file
    :param account:
    :param logger:
    :param random_name: Whether to use random name
    :param best: Whether to use the best entrypoints
    :param ipv6: Whether to use ipv6 entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account

    random_points, msg = getRandomEntryPoints(best, logger, ipv6)
    if random_points is None:
        return msg

    # Initialize NodeNameGenerator
    node_name_generator = NodeNameGenerator(random_name)

    sing_box_json = copy.deepcopy(SING_BOX)

    # Generate outbounds
    outbounds = []
    name_list = []

    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        country = GEOIP.lookup(point.ip)
        country_emoji = GEOIP.lookup_emoji(point.ip)
        name = node_name_generator.next(country_emoji, country)

        outbounds.append(
            {
                "server": point.ip,
                "server_port": point.port,
                "peers": [{
                    "server": point.ip,
                    "server_port": point.port,
                    "public_key": CF_CONFIG.get("publicKey"),
                    "pre_shared_key": "",
                    "allowed_ips": ['0.0.0.0/0', '::/0']
                }],
                "tag": name,
                "type": "wireguard",
                "local_address": ["172.16.0.2/32"],
                "private_key": account.private_key,
                "peer_public_key": CF_CONFIG.get("publicKey"),
                "system_interface": False,
                "mtu": 1280
            }
        )

        name_list.append(name)

    sing_box_json["outbounds"].extend(outbounds)

    # Section Select
    sing_box_json["outbounds"][0]["outbounds"].extend(name_list)

    # Section UrlTest
    sing_box_json["outbounds"][1]["outbounds"].extend(name_list)

    return json.dumps(sing_box_json, ensure_ascii=False)
