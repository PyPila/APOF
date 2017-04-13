from django.contrib.auth.models import User
from django.test import TestCase

from apof.portal.models import UserProfile


class UserProfileTestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create(username='christopher_sour')

    def test_user_profile_is_automatically_created(self):
        self.assertIsInstance(
            self.user.profile,
            UserProfile
        )

    def test_string_representation(self):
        self.assertEqual(str(self.user.profile), 'Profile of user: christopher_sour')

    def test_repr(self):
        self.assertEqual(
            repr(self.user.profile),
            'UserProfile(User: christopher_sour, Avatar: avatars/base.jpg)'
        )
