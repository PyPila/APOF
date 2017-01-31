import tempfile
from datetime import time

from django.test import TestCase
from django.urls import reverse

from restaurants.models import Restaurant, OpeningHours, PhoneNumber


class RestaurantTestCase(TestCase):

    def test_string_representation(self):
        test_restaurant_name = 'Test restaurant name'
        self.assertEqual(
            str(Restaurant(name=test_restaurant_name)),
            test_restaurant_name
        )


class OpeningHoursTestCase(TestCase):

    def test_string_representation(self):
        restaurant = Restaurant.objects.create(
            name='test restaurant2', logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        opening_hours = OpeningHours(
            restaurant=restaurant,
            day=0,
            opening_from=time(10),
            opening_to=time(20, 30)
        )
        self.assertEqual(str(opening_hours), 'test restaurant2 | Monday | 10:00 | 20:30')



class PhoneNumberTestCase(TestCase):

    def test_string_representation(self):
        restaurant = Restaurant.objects.create(
            name='test restaurant2', logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        phone_number = PhoneNumber(restaurant=restaurant, number='012345678')
        self.assertEqual(str(phone_number), 'test restaurant2 | 012345678')


class RestaurantListTestCase(TestCase):

    def test_restaurants_list(self):
        restaurant1 = Restaurant.objects.create(
            name='test restaurant2', logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        restaurant2 = Restaurant.objects.create(
            name='test restaurant1', logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        restaurants_list_url = reverse('restaurant-list')
        response = self.client.get(restaurants_list_url)
        self.assertEqual('/', restaurants_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/index.html')
        self.assertTemplateUsed(response, 'restaurants/base.html')
        self.assertEqual(
            [restaurant1, restaurant2], list(response.context['restaurants'])
        )
