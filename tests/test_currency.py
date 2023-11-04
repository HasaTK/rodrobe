import unittest
from src.utils import currency


class CurrencyTests(unittest.TestCase):

    def setUp(self):
        self.rate = 3.5

    def test_robux_to_usd(self):
        self.assertEqual(currency.robux_price(robux=10000, rate=self.rate), 35.0)

    def test_usd_to_robux(self):
        self.assertEqual(currency.currency_to_robux(amount=35, rate=self.rate), 10000)
