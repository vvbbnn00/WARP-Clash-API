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
