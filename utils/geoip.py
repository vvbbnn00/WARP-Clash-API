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
import maxminddb


def countryCodeToEmoji(country_code):
    """
    Convert country code to emoji.
    :param country_code: A two-letter country code
    :return: Corresponding country flag emoji if valid, otherwise a globe emoji
    """
    if not country_code or len(country_code) != 2:
        return '🌏'

    OFFSET = 127462 - ord('A')
    return chr(ord(country_code[0].upper()) + OFFSET) + chr(ord(country_code[1].upper()) + OFFSET)


class GeoIP:
    def __init__(self, db_path: str) -> None:
        self.db = maxminddb.open_database(db_path)

    def lookup(self, ip: str) -> str or None:
        """
        Lookup ip to get country code
        :param ip:
        :return:
        """

        # Remove brackets from IPv6 addresses
        if ip.startswith('['):
            ip = ip.replace('[', '').replace(']', '')

        result = self.db.get(ip)
        try:
            if result:
                # Country field shows the accurate country code of the IP
                if 'country' in result:
                    return result['country']['iso_code']
                # If no country field, use the registered_country field
                return result['registered_country']['iso_code']
            else:
                return None
        except Exception as e:
            logging.error(f"Failed to lookup ip: {ip}, error: {e}")
            return None

    def lookup_emoji(self, ip: str) -> str or None:
        """
        Lookup ip to get country emoji
        :param ip:
        :return:
        """
        result = self.lookup(ip)
        return countryCodeToEmoji(result)

    def close(self) -> None:
        """
        Close database
        :return:
        """
        self.db.close()
