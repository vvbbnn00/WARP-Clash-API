import copy
import json
import random
import yaml
import configparser
import string
import tempfile

from faker import Faker
from config import *
from services.common import *
from utils.entrypoints import getEntrypoints, getBestEntrypoints
from flask import request

CF_CONFIG = json.load(open("./config/cf-config.json", "r", encoding="utf8"))
CLASH = json.load(open("./config/clash.json", "r", encoding="utf8"))

SURGE = configparser.ConfigParser()
SURGE.read("./config/surge.conf", encoding="utf8")
SURGE_RULE = open("./config/surge-rule.txt", "r", encoding="utf8").read()
SURGE_SUB = open("./config/surge-sub.txt", "r", encoding="utf8").read()


def generateClashSubFile(account: Account = None,
                         logger=logging.getLogger(__name__),
                         best=False,
                         only_proxies=False,
                         random_name=False):
    """
    Generate Clash subscription file
    :param random_name: Whether to use random name
    :param only_proxies: If this is True, only generate proxies
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = getEntrypoints()
    random_points = random.sample(entrypoints, RANDOM_COUNT) if not best else getBestEntrypoints(RANDOM_COUNT)

    fake = Faker()

    # Generate user configuration file
    user_config = []

    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        name = f"{fake.emoji()} CF-{fake.color_name()}" if random_name else f"CF-WARP-{i + 1}"
        user_config.append(
            {
                "name": name,
                "type": "wireguard",
                "server": point.ip,
                "port": point.port,
                "ip": "172.16.0.2",
                "private-key": account.private_key,
                "public-key": CF_CONFIG.get("publicKey"),
                "remote-dns-resolve": False,
                "udp": False
            })
    clash_json = copy.deepcopy(CLASH)
    clash_json["proxies"] = user_config
    for proxy_group in clash_json["proxy-groups"]:
        proxy_group["proxies"] += [proxy["name"] for proxy in user_config]

    # Generate YAML file
    if only_proxies:
        clash_yaml = yaml.dump({'proxies': clash_json['proxies'], 'proxy-groups': clash_json['proxy-groups']},
                               allow_unicode=True)
    else:
        clash_yaml = yaml.dump(clash_json, allow_unicode=True)
    return clash_yaml


def generateWireguardSubFile(account: Account = None, logger=logging.getLogger(__name__), best=False):
    """
    Generate Wireguard subscription file
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = getEntrypoints()
    random_point = random.choice(entrypoints) if not best else getBestEntrypoints(1)[0]

    # Generate user configuration file
    text = f"""[Interface]
PrivateKey = {account.private_key}
Address = 172.16.0.2/32
DNS = 1.1.1.1
MTU = 1280

[Peer]
PublicKey = {CF_CONFIG.get("publicKey")}
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = {random_point.ip}:{random_point.port}
PersistentKeepalive = 25
"""
    return text


def generateSurgeSubFile(account: Account = None,
                         logger=logging.getLogger(__name__),
                         best=False,
                         only_proxies=False,
                         random_name=False):
    """
    Generate Surge subscription file
    :param random_name: Whether to use random name
    :param only_proxies: If this is True, only generate proxies
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = getEntrypoints()
    random_points = random.sample(entrypoints, RANDOM_COUNT) if not best else getBestEntrypoints(RANDOM_COUNT)

    fake = Faker()

    # Generate user configuration file
    user_config = []

    # Use len() instead of RANDOM_COUNT because the entrypoints may be less than RANDOM_COUNT
    for i in range(len(random_points)):
        point = random_points[i]
        user_config.append(
            {
                "self-ip": point.ip,
                "private-key": account.private_key,
                "dns-server": "1.1.1.1",
                "mtu": 1420,
                "peer": f'(public-key = {CF_CONFIG.get("publicKey")}, allowed-ips = "0.0.0.0/0, ::/0", endpoint = {point.ip}:{point.port})'
            })

    surge_config = copy.deepcopy(SURGE)

    for i, config in enumerate(user_config):
        # random a name like 2FDEC93F, num and upper letter
        name = ''.join(random.sample(string.ascii_uppercase + string.digits, 8))

        surge_config[f'WireGuard {name}'] = config
        surge_config['Proxy'][
            f"{fake.emoji()} CF-{fake.color_name()}" if random_name else f"CF-WARP-{i + 1}"] = (f'wireguard, '
                                                                                                f'section-name={name}')

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
    if only_proxies:
        pass
    else:
        surge_ini += SURGE_RULE

    # Generate subscription link, use public_url if it is not None
    public_url = PUBLIC_URL
    if public_url is None:
        # Get public url from request
        public_url = request.url_root[:-1]

    surge_ini = SURGE_SUB.replace("{PUBLIC_URL}",
                                  f"{public_url}/api/surge?best={str(best).lower()}&randomName={str(random_name).lower()}") + surge_ini

    return surge_ini
