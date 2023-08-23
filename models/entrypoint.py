import datetime


class Entrypoint:
    ip_type: str = "ipv4"
    ip: str = ""
    port: int = 0
    loss: float = 0
    delay: int = 0
    last_check: datetime.datetime = datetime.datetime.now()

    def __str__(self):
        return f"IP Type: {self.ip_type}\n" \
               f"IP: {self.ip}\n" \
               f"Port: {self.port}\n" \
               f"Loss: {self.loss}\n" \
               f"Delay: {self.delay}\n" \
               f"Last Check: {self.last_check}\n"

    def __repr__(self):
        return f"{self.ip}:{self.port}"
