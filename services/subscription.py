import json
import random
import yaml

from faker import Faker
from config import *
from services.common import *
from utils.entrypoints import get_entrypoints

CF_CONFIG = json.load(open("./config/cf-config.json", "r", encoding="utf8"))
CLASH = json.load(open("./config/clash.json", "r", encoding="utf8"))


def generate_WARP_subFile(account: Account = None, logger=logging.getLogger(__name__)):
    account = getCurrentAccount(logger) if account is None else account
    entrypoints = get_entrypoints()
    random_points = random.sample(entrypoints, RANDOM_COUNT)

    fake = Faker()

    # Generate user configuration file
    user_config = []
    for i in range(RANDOM_COUNT):
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
                "udp": True
            })
    clashJSON = CLASH.copy()
    clashJSON["proxies"] = user_config
    clashJSON["proxy-groups"][1]["proxies"] = [i.get("name") for i in user_config]
    clashJSON["proxy-groups"][2]["proxies"] = [i.get("name") for i in user_config]

    # Generate YAML file
    clashYAML = yaml.dump(clashJSON, allow_unicode=True)
    return clashYAML
