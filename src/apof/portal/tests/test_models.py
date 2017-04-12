from django.contrib.auth.models import User
from django.test import TestCase


class UserProfileTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        self.user = User.objects.get(username='christopher')

    def test_string_representation(self):
        self.assertEqual(str(self.user.profile), 'Profile of user: christopher')

    def test_repr(self):
        self.assertEqual(
            repr(self.user.profile),
            'UserProfile(User: christopher, Avatar: avatars/base.jpg)'
        )
