from datetime import time

from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from mock import patch, MagicMock

from restaurants.models import Restaurant, OpeningHours, PhoneNumber


file_mock = MagicMock(spec=File, name='FileMock')
file_mock.name = 'test1.jpg'


class RestaurantTestCase(TestCase):

    def test_string_representation(self):
        test_restaurant_name = 'Test restaurant name'
        self.assertEqual(
            str(Restaurant(name=test_restaurant_name)),
            test_restaurant_name
        )


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

    @patch('django.core.files.storage.default_storage._wrapped')
    def test_restaurants_list(self, mocked_storage):
        restaurant1 = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        restaurant2 = Restaurant.objects.create(name='test restaurant1', logo=file_mock)
        restaurants_list_url = reverse('restaurant-list')
        response = self.client.get(restaurants_list_url)
        self.assertEqual('/restaurants/', restaurants_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/index.html')
        self.assertTemplateUsed(response, 'portal/base.html')
        self.assertEqual(
            [restaurant1, restaurant2], list(response.context['restaurants'])
        )
