from django.test import TestCase

from .models import Restaurant


class TestRestaurant(TestCase):
    """Tests from Restaurant model"""
    def test_string_representation(self):
        """Tests restaurnat string representation equals it's name"""
        test_restaurant_name = 'Test restaurant name'
        self.assertEquals(
            str(Restaurant(name=test_restaurant_name)),
            test_restaurant_name
        )
