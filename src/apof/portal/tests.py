from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class IndexTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='christopher',
            email='christopher@wp.pl',
        )

    def test_anonymous_user_is_redirected_to_login_view(self):
        index_url = reverse('home')
        response = self.client.get(index_url)
        self.assertRedirects(
            response,
            reverse('login') +
            '?next=' +
            reverse('home')
        )

    def test_logged_user_is_not_redirected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class LoginTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='christopher',
            email='christopher@wp.pl',
        )

    def test_anonymous_user_is_not_redirected(self):
        index_url = reverse('login')
        response = self.client.get(index_url)
        self.assertEqual(response.status_code, 200)

    def test_logged_user_is_redirected_to_index_view(self):
        self.client.force_login(self.user)
        index_url = reverse('login')
        response = self.client.get(index_url)
        self.assertRedirects(response, reverse('home'))
