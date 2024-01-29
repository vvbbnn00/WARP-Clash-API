import logging

from models import Account
from services.cloudflare import register
from utils.wireguard import generateWireguardKeys


def getCurrentAccount(logger=logging.Logger(__name__)):
    """
    Get current account
    :param logger: 
    :return:
    """
    logger.info(f"Get current account")
    try:
        account = Account.load()
    except FileNotFoundError:
        account = None
    if account is None:
        logger.info(f"No account found, register a new one")
        privkey, pubkey = generateWireguardKeys()
        account = register(pubkey, privkey)
        account.save()
    # Avoid returning None in headers
    account.usage = account.usage if account.usage is not None else 0
    account.quota = account.quota if account.quota is not None else 0
    return account
