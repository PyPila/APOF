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

    @patch('django.core.files.storage.default_storage._wrapped')
    def setUp(self, mocked_storage):
        self.restaurant = Restaurant.objects.create(
            name='Test',
            logo=file_mock
        )

    def test_string_representation(self):
        self.assertEqual(
            str(self.restaurant),
            'Test'
        )

    def test_repr(self):
        self.assertEqual(
            repr(self.restaurant),
            'Restaurant(Name: Test)'
        )

    def test_get_phone_numbers(self):
        number1 = '012345678'
        number2 = '876543210'
        expected_result = [number1, number2]

        PhoneNumber.objects.bulk_create([
            PhoneNumber(restaurant=self.restaurant, number=number1),
            PhoneNumber(restaurant=self.restaurant, number=number2)
        ])
        result = self.restaurant.get_phone_numbers()
        self.assertEqual(expected_result, result)


class OpeningHoursTestCase(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test',
        )
        self.opening_hours = OpeningHours.objects.create(
            restaurant=self.restaurant,
            day=0,
            opening_from=time(10),
            opening_to=time(20, 30)
        )

    def test_string_representation(self):
        self.assertEqual(str(self.opening_hours), 'Test | Monday | 10:00 | 20:30')

    def test_repr(self):
        self.assertEqual(
            repr(self.opening_hours),
            'OpeningHours(Restaurant: Test, Day: 0)'
        )


class PhoneNumberTestCase(TestCase):

    def setUp(self):
        self.restaurant = Restaurant.objects.create(
            name='Test',
        )
        self.phone_number = PhoneNumber.objects.create(
            restaurant=self.restaurant,
            number='012345678'
        )

    def test_string_representation(self):
        self.assertEqual(str(self.phone_number), 'Test | 012345678')

    def test_repr(self):
        self.assertEqual(
            repr(self.phone_number),
            'PhoneNumber(Restaurant: Test, Number: 012345678)'
        )


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
