import unittest

from src.config import cfg_file
from src.clients import accounts


class AccountTest(unittest.TestCase):

    def setUp(self):
        self.holder_cookie = cfg_file["group"]["holder_cookie"]
        self.uploader_cookie = cfg_file["group"]["uploader_cookie"]

    def test_holder_cookie(self):
        self.assertTrue(
            accounts.RobloxAccount(cookie=self.holder_cookie).getClientInfo(),
            msg="Holder cookie is invalid"
        )

    def test_uploader_cookie(self):
        self.assertTrue(
            accounts.RobloxAccount(cookie=self.uploader_cookie).getClientInfo(),
            msg="Uploader cookie is invalid"
        )
