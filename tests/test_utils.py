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
import unittest

from utils.entrypoints import *
from utils.geoip import GeoIP, countryCodeToEmoji
from utils.proxy import getProxy
from utils.wireguard import generateWireguardKeys

# Change working directory to the root directory
os.chdir(os.path.join(os.path.dirname(__file__), ".."))


class TestUtils(unittest.TestCase):
    def test_getProxy(self):
        proxy = getProxy()
        self.assertTrue(proxy.get("http") or proxy.get("https"))

    def test_Wireguard(self):
        privkey, pubkey = generateWireguardKeys()
        self.assertTrue(privkey)
        self.assertTrue(pubkey)
        self.assertEqual(len(privkey), 44)
        self.assertEqual(len(pubkey), 44)

    def test_EntryPoints(self):
        reloadEntrypoints()
        entrypoints = getEntrypoints()
        self.assertTrue(entrypoints)
        self.assertTrue(len(entrypoints) > 0)

    def test_GeoIP(self):
        geoip = GeoIP('./config/geolite/GeoLite2-Country.mmdb')
        country = geoip.lookup('8.8.8.8')
        self.assertTrue(country)
        self.assertEqual(country, "US")
        self.assertEqual(countryCodeToEmoji(country), "🇺🇸")

        countryNone = geoip.lookup('127.0.0.1')
        self.assertFalse(countryNone)
        self.assertEqual(countryCodeToEmoji(countryNone), "🌏")

        geoip.close()


if __name__ == '__main__':
    unittest.main()
