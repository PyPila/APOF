import tempfile

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

    def test_restaurants_list_view_context(self):
        restaurant1 = Restaurant.objects.create(
            name='test restaurant2', opening='10.00-18.00',
            logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        restaurant2 = Restaurant.objects.create(
            name='test restaurant', opening='14.00-22.00',
            logo=tempfile.NamedTemporaryFile(suffix='.jpg').name
        )
        response = self.client.get(reverse('restaurant-list'))
        self.assertEqual(
            [restaurant1, restaurant2], list(response.context['restaurants'])
        )
