from django.contrib.auth.models import User
from django.test import TestCase
from mock import MagicMock, Mock, patch

from apof.portal import pipeline


class PipelineTestCase(TestCase):

    def setUp(self):
        self.mock_backend = MagicMock()
        self.mock_backend.name = 'google-oauth2'
        self.mock_response = {'image': MagicMock(get=MagicMock(side_effect=['test']))}
        self.user = User.objects.create(username='christopher_sour')

    @patch('django.core.files.storage.default_storage._wrapped')
    @patch('urllib2.urlopen')
    def test_get_user_avatar(self, mock_urllib, mock_storage):
        mock_storage.url = MagicMock(name='url')
        mock_storage.url.return_value = '/tmp/test1.jpg'
        mock_storage.save = MagicMock(name='save')
        mock_storage.save.return_value = '/tmp/test1.jpg'
        mock_url = Mock()
        mock_url.read.side_effect = ['test']
        mock_urllib.return_value = mock_url

        pipeline.get_avatar(
            self.mock_backend,
            None,
            self.mock_response,
            self.user
        )
        self.assertEqual(self.user.profile.avatar.url, '/tmp/test1.jpg')
