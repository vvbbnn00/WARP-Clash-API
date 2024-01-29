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
    def __init__(self, db_path):
        self.db = maxminddb.open_database(db_path)

    def lookup(self, ip):
        """
        Lookup ip to get country code
        :param ip:
        :return:
        """
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
            return None

    def lookup_emoji(self, ip):
        """
        Lookup ip to get country emoji
        :param ip:
        :return:
        """
        result = self.lookup(ip)
        return countryCodeToEmoji(result)

    def close(self):
        """
        Close database
        :return:
        """
        self.db.close()
