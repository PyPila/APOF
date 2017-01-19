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

    def test_main_page_view_is_restaurants_list_view(self):
        self.assertEqual('/', reverse('restaurant-list'))

    def test_restaurants_list_view(self):
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'restaurants/index.html')
