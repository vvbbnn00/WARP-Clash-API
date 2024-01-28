import datetime
import requests
import faker
from models import Account

API_URL = "https://api.cloudflareclient.com"
API_VERSION = "v0a1922"
DEFAULT_HEADERS = {
    "User-Agent": "okhttp/3.12.1",
    "CF-Client-Version": "a-6.3-1922",
    'Content-Type': 'application/json; charset=UTF-8',
    'Host': 'api.cloudflareclient.com',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip',
}

SESSION = requests.Session()
SESSION.headers.update(DEFAULT_HEADERS)
FAKE = faker.Faker()


def genAccountFromResponse(response, referrer=None, private_key=None) -> Account:
    """
    Generate an account from a response
    :param private_key:
    :param response:
    :param referrer:
    :return:
    """
    account = Account()
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


def register(public_key, private_key, device_model=f"{FAKE.company()} {FAKE.country()}", referrer="",
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
    timestamp = datetime.datetime.now().isoformat()[:-3] + "+02:00"
    # install_id is 43 characters long
    install_id = FAKE.pystr(min_chars=43, max_chars=43)
    data = {
        # 152 characters in total
        "fcm_token": "{}:APA91b{}".format(install_id, FAKE.pystr(min_chars=134, max_chars=134)),
        "install_id": install_id,
        "key": public_key,
        "warp_enabled": True,
        "locale": "en_US",
        "model": device_model,
        "tos": timestamp,
        "type": FAKE.random_element(elements=("Android", "iOS")),
    }
    if referrer:
        data["referrer"] = referrer
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
    account.license_key = data["account"].get("license")
    account.premium_data = data["account"].get("premium_data")
    account.quota = data["account"].get("quota")
    account.usage = data["account"].get("usage")
    account.updated_at = data["account"].get("updated")

    return data["account"]


def getClientConfig(proxy=None) -> dict:
    """
    Get client config

    :param proxy: proxy dict
    :return:
    """

    response = SESSION.get(f"{API_URL}/{API_VERSION}/client_config",
                           proxies=proxy)
    response.raise_for_status()

    return response.json()
