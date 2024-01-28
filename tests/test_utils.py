import unittest

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


if __name__ == '__main__':
    unittest.main()
