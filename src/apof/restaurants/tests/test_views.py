from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from mock import patch, MagicMock

from apof.restaurants.models import Restaurant

file_mock = MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'


class RestaurantListTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        self.user = User.objects.get(username='christopher')

    def test_anonymous_user_is_redirected_to_login_view(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertRedirects(
            response,
            '{}{}{}'.format(reverse('login'), '?next=', reverse('restaurant-list'))
        )

    def test_logged_user_is_not_redirected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)

    @patch('django.core.files.storage.default_storage._wrapped')
    def test_restaurants_list(self, mocked_storage):
        restaurant1 = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        restaurant2 = Restaurant.objects.create(name='test restaurant1', logo=file_mock)
        restaurants_list_url = reverse('restaurant-list')
        self.client.force_login(self.user)

        response = self.client.get(restaurants_list_url)
        self.assertEqual('/restaurants/', restaurants_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/index.html')
        self.assertTemplateUsed(response, 'portal/base.html')
        self.assertEqual(
            [restaurant1, restaurant2], list(response.context['restaurants'])
        )
