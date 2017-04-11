from django.test import TestCase

from django.apps.config import AppConfig

from apof.baskets.apps import BasketsConfig


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        BasketsConfigMRO = BasketsConfig.__mro__
        expectedMRO = (BasketsConfig, AppConfig, object)
        self.assertEqual(BasketsConfigMRO, expectedMRO)
