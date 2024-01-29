import unittest

from utils.geoip import GeoIP, countryCodeToEmoji
from utils.proxy import getProxy
from utils.wireguard import generateWireguardKeys
from utils.entrypoints import *


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
        geoip = GeoIP('../config/geolite/GeoLite2-Country.mmdb')
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
