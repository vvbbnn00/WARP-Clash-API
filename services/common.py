import logging

from models import Account
from services.cloudflare import register
from utils.wireguard import generate_wireguard_keys


def getCurrentAccount(logger=logging.Logger(__name__)):
    logger.info(f"Get current account")
    try:
        account = Account.load()
    except FileNotFoundError:
        account = None
    if account is None:
        logger.info(f"No account found, register a new one")
        privkey, pubkey = generate_wireguard_keys()
        account = register(pubkey, privkey)
        account.save()
    return account
