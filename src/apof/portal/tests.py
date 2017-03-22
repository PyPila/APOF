from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from mock import MagicMock, Mock, patch

from portal import pipeline
from portal.models import UserProfile


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


class UserProfileTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_user_profile_is_automatically_created(self):
        user = User.objects.get(username='christopher')
        self.assertIsInstance(
            user.profile,
            UserProfile
        )


class PipelineTestCase(TestCase):
    """
    Tests if user get avatar inside pipeline
    """
    fixtures = ['test_user_data.json']

    def setUp(self):
        """
        Those mocks are used to set function response['image'].get('url') to
        return 'test'.
        """
        self.backend_mock = MagicMock()
        self.backend_mock.name = 'google-oauth2'
        self.response_mock = {'image': MagicMock(get=MagicMock(side_effect=['test']))}

    @patch('django.core.files.storage.default_storage._wrapped')
    @patch('urllib2.urlopen')
    def test_get_user_avatar(self, urllib_mock, storage_mock):
        storage_mock.url = MagicMock(name='url')
        storage_mock.url.return_value = '/tmp/test1.jpg'
        storage_mock.save = MagicMock(name='save')
        storage_mock.save.return_value = '/tmp/test1.jpg'
        url_mock = Mock()
        url_mock.read.side_effect = ['test']
        urllib_mock.return_value = url_mock
        user = User.objects.get(username='christopher')

        pipeline.get_avatar(
            self.backend_mock,
            None,
            self.response_mock,
            user,
        )
        self.assertEqual(
            user.profile.avatar.url,
            '/tmp/test1.jpg'
        )
