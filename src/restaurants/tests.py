import tempfile
from datetime import time

from django.test import TestCase
from django.urls import reverse

from .models import Restaurant


class RestaurantTestCase(TestCase):

    def test_string_representation(self):
        test_restaurant_name = 'Test restaurant name'
        self.assertEqual(
            str(Restaurant(name=test_restaurant_name)),
            test_restaurant_name
        )


class RestaurantListTestCase(TestCase):

    def test_restaurants_list(self):
        restaurant1 = Restaurant.objects.create(
            name='test restaurant2', opening_from=time(10), opening_to=time(18),
            logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        restaurant2 = Restaurant.objects.create(
            name='test restaurant1', opening_from=time(10), opening_to=time(18),
            logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
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
