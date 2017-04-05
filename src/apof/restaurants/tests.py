from datetime import time

from django.apps.config import AppConfig
from django.contrib.auth.models import User
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from mock import patch, MagicMock

from restaurants.models import OpeningHours, PhoneNumber, Restaurant
from restaurants.apps import RestaurantsConfig


file_mock = MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'


class RestaurantTestCase(TestCase):

    def test_string_representation(self):
        test_restaurant_name = 'Test restaurant name'
        self.assertEqual(
            str(Restaurant(name=test_restaurant_name)),
            test_restaurant_name
        )

    @patch('django.core.files.storage.default_storage._wrapped')
    def test_get_phone_numbers(self, mocked_storage):
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        number1 = '012345678'
        number2 = '876543210'
        PhoneNumber.objects.bulk_create([
            PhoneNumber(restaurant=restaurant, number=number1),
            PhoneNumber(restaurant=restaurant, number=number2)
        ])
        expected_result = [number1, number2]
        result = restaurant.get_phone_numbers()
        self.assertEqual(expected_result, result)


class OpeningHoursTestCase(TestCase):

    @patch('django.core.files.storage.default_storage._wrapped')
    def test_string_representation(self, mocked_storage):
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        opening_hours = OpeningHours(
            restaurant=restaurant,
            day=0,
            opening_from=time(10),
            opening_to=time(20, 30)
        )
        self.assertEqual(str(opening_hours), 'test restaurant2 | Monday | 10:00 | 20:30')


class PhoneNumberTestCase(TestCase):

    @patch('django.core.files.storage.default_storage._wrapped')
    def test_string_representation(self, mocked_storage):
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        phone_number = PhoneNumber(restaurant=restaurant, number='012345678')
        self.assertEqual(str(phone_number), 'test restaurant2 | 012345678')


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


class AppsTestCase(TestCase):
    def test_BasketConfig_mro(self):
        RestaurantsConfigMRO = RestaurantsConfig.__mro__
        expectedMRO = (RestaurantsConfig, AppConfig, object)
        self.assertEqual(RestaurantsConfigMRO, expectedMRO)
