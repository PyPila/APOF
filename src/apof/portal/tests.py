from django.apps.config import AppConfig
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from portal.apps import PortalConfig

class IndexTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_anonymous_user_is_redirected_to_login_view(self):
        response = self.client.get(reverse('home'))
        self.assertRedirects(
            response,
            '{}{}{}'.format(reverse('login'), '?next=', reverse('home'))
        )

    def test_logged_user_is_not_redirected(self):
        self.client.force_login(User.objects.get(username='christopher'))
        response = self.client.get(reverse('home'))
        self.assertRedirects(response, '/restaurants/')


class LoginTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_anonymous_user_is_not_redirected(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_logged_user_is_redirected_to_restaurant_view(self):
        self.client.force_login(User.objects.get(username='christopher'))
        response = self.client.get(reverse('login'))
        self.assertRedirects(
            response,
            reverse('home'),
            status_code=302,
            target_status_code=302
        )


class LogoutTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_user_logout(self):
        self.client.force_login(User.objects.get(username='christopher'))
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('home'))
        self.assertRedirects(
            response,
            '{}{}{}'.format(reverse('login'), '?next=', reverse('home'))
        )


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        PortalConfigMRO = PortalConfig.__mro__
        expectedMRO = (PortalConfig, AppConfig, object)
        self.assertEqual(PortalConfigMRO, expectedMRO)
