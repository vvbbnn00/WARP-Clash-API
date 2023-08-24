import copy
import json
import random
import yaml

from faker import Faker
from config import *
from services.common import *
from utils.entrypoints import get_entrypoints, get_best_entrypoints

CF_CONFIG = json.load(open("./config/cf-config.json", "r", encoding="utf8"))
CLASH = json.load(open("./config/clash.json", "r", encoding="utf8"))


def generate_Clash_subFile(account: Account = None, logger=logging.getLogger(__name__), best=False):
    """
    Generate Clash subscription file
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
                "name": f"{fake.emoji()} CF-{fake.color_name()}",
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
"""
    return text
