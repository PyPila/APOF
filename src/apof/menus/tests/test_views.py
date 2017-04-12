from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class MealListViewTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        self.user = User.objects.get(username='christopher')

    def test_anonymous_user_is_redirected_to_login_view(self):
        response = self.client.get(reverse('meal-list', kwargs={'restaurant_pk': 1}))

        redirect_url = '{}{}{}'.format(
            reverse('login'),
            '?next=',
            reverse(
                'meal-list',
                kwargs={'restaurant_pk': 1}
            )
        )
        self.assertRedirects(response, redirect_url)

    def test_logged_user_is_not_redirected(self):
        self.client.force_login(self.user)

        response = self.client.get(reverse('meal-list', kwargs={'restaurant_pk': 1}))
        self.assertEqual(response.status_code, 200)
