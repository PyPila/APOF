from django.apps.config import AppConfig
from django.test import TestCase

from apof.portal.apps import PortalConfig


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        PortalConfigMRO = PortalConfig.__mro__
        expectedMRO = (PortalConfig, AppConfig, object)
        self.assertEqual(PortalConfigMRO, expectedMRO)
