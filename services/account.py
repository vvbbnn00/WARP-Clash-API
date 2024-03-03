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

from services.cloudflare import updatePublicKey, updateLicenseKey
from services.common import getCurrentAccount
from utils.wireguard import generateWireguardKeys


def resetAccountKey(logger=logging.Logger(__name__)):
    """
    Reset account private key, and update public key to Cloudflare
    :param logger:
    :return:
    """
    # Get current account
    account = getCurrentAccount(logger)
    logger.info(f"Reset account key for account: {account.account_id}")

    # Generate new keys
    privkey, pubkey = generateWireguardKeys()
    updatePublicKey(account, pubkey)
    logger.info(f"New public key: {pubkey}")
    logger.info(f"New private key: {privkey}")

    # Save new private key
    account.private_key = privkey
    # Save account to file
    account.save()

    logger.info("Account key reset done")


def doUpdateLicenseKey(license_key: str, logger=logging.Logger(__name__)):
    """
    Update license key, and reset account key
    :param license_key:
    :param logger:
    :return:
    """
    logger.info(f"Update license key: {license_key}")

    # Get current account
    account = getCurrentAccount(logger)

    if account.license_key == license_key:
        logger.warning("License key is the same, no need to update")
        return

    # Update license key
    updateLicenseKey(account, license_key, logger=logger)

    # Save changes to account
    account.license_key = license_key
    account.save()

    # Account needs to be reset after license key update
    resetAccountKey(logger)

    logger.info("License key updated")
