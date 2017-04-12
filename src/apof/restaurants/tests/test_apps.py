from django.apps.config import AppConfig
from django.test import TestCase

from apof.restaurants.apps import RestaurantsConfig


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        self.assertEqual(
            RestaurantsConfig.__mro__,
            (
                RestaurantsConfig,
                AppConfig,
                object
            )
        )
