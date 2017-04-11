from django.apps.config import AppConfig
from django.test import TestCase

from apof.portal.apps import PortalConfig


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        self.assertEqual(
            PortalConfig.__mro__,
            (PortalConfig, AppConfig, object)
        )
