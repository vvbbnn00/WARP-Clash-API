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
import logging
import sys
import time

from models import Account
from services.cloudflare import register
from services.common import getCurrentAccount
from utils.entrypoints import optimizeEntrypoints
from utils.wireguard import generateWireguardKeys
from services.cloudflare import getAccount
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
        privkey, pubkey = generateWireguardKeys()
        register(pubkey, privkey, referrer=account.account_id, proxy=getProxy())
    except Exception as e:
        logger.warning("Failed to get account from Cloudflare.")
        logger.warning(f"{e}")
        return False

    end = time.time()

    logger.info("Got account from Cloudflare")
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
    info = getAccount(account)
    logger.info(f"Account info: {info}")
    logger.info("Save account to file")
    account.save()


def reoptimizeEntryPoints(logger=logging.Logger(__name__)):
    """
    Reoptimize entrypoints
    :param logger:
    :return:
    """
    if sys.platform == "win32":
        logger.warning("Reoptimize is not supported on Windows.")
        return

    logger.info("Start reoptimize entrypoints.")

    try:
        optimizeEntrypoints()
    except Exception as e:
        logger.error("Failed to reoptimize entrypoints.")
        logger.error(f"{e}")

    logger.info("Reoptimize entrypoints finished.")

# if __name__ == '__main__':
#     privkey, pubkey = generate_wireguard_keys()
#     account = register(pubkey, privkey, proxy=getProxy())
#     print(account)
#     privkey, pubkey = generate_wireguard_keys()
#     new_account = register(pubkey, privkey, proxy=getProxy(), referrer=account.account_id)
#     print(new_account)
