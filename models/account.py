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
import json
import logging

ACCOUNT_PATH = "account/account.json"


class Account:
    account_id: str = ""
    account_type: str = ""
    created_at: datetime.datetime = datetime.datetime.now()
    updated_at: datetime.datetime = datetime.datetime.now()
    model: str = ""
    referrer: str = ""
    private_key: str = ""
    license_key: str = ""
    token: str = ""
    premium_data: int = 0
    quota: int = 0
    usage: int = 0

    def __str__(self):
        return f"Account ID: {self.account_id}\n" \
               f"Account Type: {self.account_type}\n" \
               f"Created At: {self.created_at}\n" \
               f"Updated At: {self.updated_at}\n" \
               f"Model: {self.model}\n" \
               f"Referrer: {self.referrer}\n" \
               f"Private Key: {self.private_key}\n" \
               f"License Key: {self.license_key}\n" \
               f"Token: {self.token}\n" \
               f"Premium Data: {self.premium_data}\n" \
               f"Quota: {self.quota}\n" \
               f"Used: {self.usage}\n"

    def save(self, file=ACCOUNT_PATH):
        with open(file, "w") as f:
            json.dump(self.__dict__, f)

    @staticmethod
    def load(file=ACCOUNT_PATH):
        try:
            with open(file, "r") as f:
                data = json.load(f)
                account = Account()
                account.__dict__ = data
                return account
        except Exception as e:
            logging.error(f"Failed to load account from file: {e}")
            return None
