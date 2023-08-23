import unittest

from utils.proxy import getProxy
from utils.wireguard import generate_wireguard_keys
from utils.entrypoints import *


class TestUtils(unittest.TestCase):
    def test_getProxy(self):
        proxy = getProxy()
        self.assertTrue(proxy.get("http") or proxy.get("https"))

    def test_Wireguard(self):
        privkey, pubkey = generate_wireguard_keys()
        self.assertTrue(privkey)
        self.assertTrue(pubkey)
        self.assertEqual(len(privkey), 44)
        self.assertEqual(len(pubkey), 44)

    def test_EntryPoints(self):
        reload_entrypoints()
        entrypoints = get_entrypoints()
        self.assertTrue(entrypoints)
        self.assertTrue(len(entrypoints) > 0)


if __name__ == '__main__':
    unittest.main()
