import logging
import time

from models import Account
from services.cloudflare import register
from services.common import getCurrentAccount
from utils.wireguard import generate_wireguard_keys
from services.cloudflare import get_account
from utils.proxy import getProxy


def doAddDataTaskOnce(account: Account = None, logger=logging.Logger(__name__)) -> bool:
    """
    Add data task once
    :param account:
    :param logger:
    :return:
    """

    if account is None:
        account = getCurrentAccount(logger)

    logger.info(f"WORK ON ID: {account.account_id}")
    start = time.time()

    try:
        privkey, _ = generate_wireguard_keys()
        register(privkey, referrer=account.account_id, proxy=getProxy())
    except Exception as e:
        logger.warning(f"Failed to get account from Cloudflare.")
        logger.warning(f"{e}")
        return False

    end = time.time()

    logger.info(f"Got account from Cloudflare")
    logger.info(f"Time used: {end - start:.2f}s")

    return True


def saveAccount(account: Account = None, logger=logging.Logger(__name__)):
    """
    Save latest account info to file
    :param account:
    :param logger:
    :return:
    """

    if account is None:
        account = getCurrentAccount(logger)

    # Get new account info
    info = get_account(account)
    logger.info(f"Account info: {info}")
    logger.info(f"Save account to file")
    account.save()
