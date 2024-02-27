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
import datetime
import random

import requests
import faker
from models import Account

API_URL = "https://api.cloudflareclient.com"
API_VERSION = "v0i2308311933"
DEFAULT_HEADERS = {
    "User-Agent": "1.1.1.1/6.23",
    "CF-Client-Version": "i-6.23-2308311933.1",
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'api.cloudflareclient.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
}

SESSION = requests.Session()
SESSION.headers.update(DEFAULT_HEADERS)
FAKE = faker.Faker()
LOCALE_LIST = ["en_US", "zh_CN", "zh_TW", "ja_JP", "ko_KR", "fr_FR", "de_DE", "es_ES"]
DEVICE_MODEL_LIST = ["iPhone16,2", "iPhone16,1", "iPhone14,2", "iPhone14,1", "iPhone13,4", "iPhone13,3", "iPhone13,2",
                     "iPhone13,1", "iPhone12,8", "iPhone12,5", "iPhone12,3", "iPhone12,1", "iPhone11,8", "iPhone11,6",
                     "iPhone11,4", "iPhone11,2", "iPhone10,6", "iPhone10,5", "iPhone10,4", "iPhone10,3", "iPhone10,2",
                     "iPhone10,1", "iPad8,8", "iPad8,7", "iPad8,6", "iPad8,5", "iPad8,4", "iPad8,3", "iPad8,2",
                     "iPad8,1", "iPad7,6", "iPad7,5", "iPad7,4", "iPad7,3", "iPad7,2", "iPad7,1", "iPad6,12",
                     "iPad6,11", "iPad5,4", "iPad5,3", "iPad5,2", "iPad5,1"]


def genAccountFromResponse(response, referrer=None, private_key=None) -> Account:
    """
    Generate an account from a response
    :param private_key:
    :param response:
    :param referrer:
    :return:
    """
    account = Account()
    response = response["result"]

    account.model = response["model"]
    account.account_id = response["id"]
    account.account_type = response["account"]["account_type"]
    account.token = response["token"]
    account.private_key = private_key
    account.license_key = response["account"]["license"]
    account.created_at = response["account"]["created"]
    account.updated_at = response["account"]["updated"]
    account.premium_data = response["account"]["premium_data"]
    account.quota = response["account"]["quota"]
    account.usage = response["account"]["usage"]
    account.referrer = referrer

    return account


def register(public_key, private_key, device_model=None, referrer="",
             proxy=None) -> Account:
    """
    Register a new device

    :param private_key: base64 encoded private key
    :param proxy: proxy dict
    :param referrer: referrer ID, optional
    :param public_key: base64 encoded public key
    :param device_model: device model
    :return:
    """
    timestamp = datetime.datetime.now().isoformat()[:-3] + "Z"
    # install_id is 43 characters long
    install_id = FAKE.pystr(min_chars=43, max_chars=43)

    # if device_model is not provided, choose a random one
    if device_model is None:
        device_model = random.choice(DEVICE_MODEL_LIST)

    data = {
        # 152 characters in total
        "fcm_token": "{}:APA91b{}".format(install_id, FAKE.pystr(min_chars=134, max_chars=134)),
        "install_id": install_id,
        "key": public_key,
        "warp_enabled": True,
        "locale": random.choice(LOCALE_LIST),
        "model": device_model,
        "tos": timestamp,
        "type": "IOS",
    }

    if referrer:
        data["referrer"] = referrer

    # Send the request
    response = SESSION.post(f"{API_URL}/{API_VERSION}/reg", json=data, proxies=proxy)
    response.raise_for_status()

    return genAccountFromResponse(response.json(), referrer=referrer, private_key=private_key)


def getAccount(account: Account, proxy=None) -> dict:
    """
    Get account details and update the account object

    :param account: account
    :param proxy: proxy dict
    :return:
    """

    response = SESSION.get(f"{API_URL}/{API_VERSION}/reg/{account.account_id}",
                           headers={"Authorization": f"Bearer {account.token}"},
                           proxies=proxy)
    response.raise_for_status()
    data = response.json()
    data = data["result"]

    account.license_key = data["account"].get("license")
    account.premium_data = data["account"].get("premium_data")
    account.quota = data["account"].get("quota")
    account.usage = data["account"].get("usage")
    account.updated_at = data["account"].get("updated")

    return data["account"]


def updateLicenseKey(account: Account, license_key: str, proxy=None, logger=None) -> dict:
    """
    Update license key

    :param account: account
    :param license_key: license key
    :param proxy: proxy dict
    :param logger: logger
    :return:
    """
    timestamp = datetime.datetime.now().isoformat()[:-3] + "Z"

    data = {
        "tos": timestamp,
        "license": license_key,
    }

    response = SESSION.put(f"{API_URL}/{API_VERSION}/reg/{account.account_id}/account",
                           headers={"Authorization": f"Bearer {account.token}"},
                           json=data, proxies=proxy)

    if response.status_code >= 400:
        if logger:
            logger.error(f"Failed to update license key, response: {response.text}")

    response.raise_for_status()

    return response.json()["result"]


def updatePublicKey(account: Account, public_key: str, proxy=None) -> dict:
    """
    Update public key

    :param account: account
    :param public_key: public key
    :param proxy: proxy dict
    :return:
    """
    data = {
        "key": public_key
    }

    response = SESSION.put(f"{API_URL}/{API_VERSION}/reg/{account.account_id}",
                           headers={"Authorization": f"Bearer {account.token}"},
                           json=data, proxies=proxy)
    response.raise_for_status()

    return response.json()["result"]


def getClientConfig(proxy=None) -> dict:
    """
    Get client config

    :param proxy: proxy dict
    :return:
    """

    response = SESSION.get(f"{API_URL}/{API_VERSION}/client_config",
                           proxies=proxy)
    response.raise_for_status()

    return response.json()["result"]
