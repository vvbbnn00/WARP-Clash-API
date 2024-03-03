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

from models import Account
from services.cloudflare import register
from utils.wireguard import generateWireguardKeys


def getCurrentAccount(logger=logging.Logger(__name__)):
    """
    Get current account
    :param logger: 
    :return:
    """
    logger.info("Get current account")
    try:
        account = Account.load()
    except FileNotFoundError:
        account = None
    if account is None:
        logger.info("No account found, register a new one")
        privkey, pubkey = generateWireguardKeys()
        account = register(pubkey, privkey)
        account.save()
    # Avoid returning None in headers
    account.usage = account.usage if account.usage is not None else 0
    account.quota = account.quota if account.quota is not None else 0
    return account
