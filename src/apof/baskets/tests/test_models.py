from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from apof.baskets.models import Basket
from apof.baskets.tests.utils import OrderTestMixin


class BasketTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        self.basket = Basket(owner=User.objects.get(username='christopher'))

    def test_string_representation(self):
        self.assertEqual(str(self.basket), 'Basket christopher')

    def test_repr(self):
        self.assertEqual(repr(self.basket), 'Basket (Owner: christopher)')


class OrderTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        self.assertEqual(str(self.order), 'christopher test_meal')

    def test_get_restaurant(self):
        self.assertEqual(self.order.get_restaurant_name(), 'test restaurant2')

    def test_get_total_price(self):
        self.assertEqual(self.order.get_total_price(), Decimal('26.74'))

    def test_repr(self):
        self.assertEqual(
            repr(self.order),
            'Order (Basket: 17, Restaurant: test restaurant2, Meal: test_meal)'
        )
