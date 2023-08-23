import datetime
import json

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
            return None
