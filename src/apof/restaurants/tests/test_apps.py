from django.apps.config import AppConfig
from django.test import TestCase

from apof.restaurants.apps import RestaurantsConfig


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        RestaurantsConfigMRO = RestaurantsConfig.__mro__
        expectedMRO = (RestaurantsConfig, AppConfig, object)
        self.assertEqual(RestaurantsConfigMRO, expectedMRO)
