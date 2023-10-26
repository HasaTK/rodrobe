import unittest
from random import choice
from src.utils import assets


class AssetsTest(unittest.TestCase):
    def setUp(self):
        self.asset_id = 607785314

    def test_asset_details(self):
        self.assertTrue(assets.getAssetDetails(self.asset_id))

    def test_grouped_asset_details(self):
        self.assertTrue(assets.getGroupedAssetDetails(
            asset_list=[self.asset_id, 398633584, 398634295, 398635081, 4047884046]
        ))

    def test_fp_scraper(self):
        self.assertTrue(assets.get_fp_assets(
            subcategory=choice(["ClassicShirts", "ClassicPants"]),
            limit=10,
        ))

    def test_byte_fetcher(self):
        self.assertTrue(assets.fetchAssetBytes(self.asset_id))
