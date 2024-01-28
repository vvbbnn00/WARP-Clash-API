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
from utils.entrypoints import get_entrypoints, get_best_entrypoints

CF_CONFIG = json.load(open("./config/cf-config.json", "r", encoding="utf8"))
CLASH = json.load(open("./config/clash.json", "r", encoding="utf8"))

SURGE = configparser.ConfigParser()
SURGE.read("./config/surge.conf", encoding="utf8")
SURGE_RULE = open("./config/surge-rule.txt", "r", encoding="utf8").read()


def generate_Clash_subFile(account: Account = None,
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
    entrypoints = get_entrypoints()
    random_points = random.sample(entrypoints, RANDOM_COUNT) if not best else get_best_entrypoints(RANDOM_COUNT)

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
    clashJSON = copy.deepcopy(CLASH)
    clashJSON["proxies"] = user_config
    for proxyGroup in clashJSON["proxy-groups"]:
        proxyGroup["proxies"] += [proxy["name"] for proxy in user_config]

    # Generate YAML file
    if only_proxies:
        clashYAML = yaml.dump({'proxies': clashJSON['proxies'], 'proxy-groups': clashJSON['proxy-groups']},
                              allow_unicode=True)
    else:
        clashYAML = yaml.dump(clashJSON, allow_unicode=True)
    return clashYAML


def generate_Wireguard_subFile(account: Account = None, logger=logging.getLogger(__name__), best=False):
    """
    Generate Wireguard subscription file
    :param account:
    :param logger:
    :param best: Whether to use the best entrypoints
    :return:
    """
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = get_entrypoints()
    random_point = random.choice(entrypoints) if not best else get_best_entrypoints(1)[0]

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


def generate_Surge_subFile(account: Account = None,
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
    entrypoints = get_entrypoints()
    random_points = random.sample(entrypoints, RANDOM_COUNT) if not best else get_best_entrypoints(RANDOM_COUNT)

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

    surgeConfig = copy.deepcopy(SURGE)

    for i, config in enumerate(user_config):
        # random a name like 2FDEC93F, num and upper letter
        name = ''.join(random.sample(string.ascii_uppercase + string.digits, 8))

        surgeConfig[f'WireGuard {name}'] = config
        surgeConfig['Proxy'][
            f"{fake.emoji()} CF-{fake.color_name()}" if random_name else f"CF-WARP-{i + 1}"] = (f'wireguard, '
                                                                                                f'section-name={name}')

    surgeConfig['Proxy Group']['proxy'] = f"select, auto, fallback, {', '.join(surgeConfig['Proxy'].keys())}"
    surgeConfig['Proxy Group'][
        'auto'] = (f"url-test, {', '.join(surgeConfig['Proxy'].keys())}, url=http://www.gstatic.com/generate_204, "
                   f"interval=43200")
    surgeConfig['Proxy Group'][
        'fallback'] = (f"fallback, {', '.join(surgeConfig['Proxy'].keys())}, url=http://www.gstatic.com/generate_204, "
                       f"interval=43200")

    # generate a tmp file to store the path of surge.ini
    temp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False, encoding='utf8')
    surgeConfig.write(temp_file)
    temp_file.seek(0)
    surgeINI = temp_file.read()

    # Generate INI file
    if only_proxies:
        pass
    else:
        surgeINI += SURGE_RULE

    return surgeINI
