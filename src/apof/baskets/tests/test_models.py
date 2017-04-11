from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from apof.baskets.models import Basket, Order
from apof.baskets.tests.utils import OrderTestMixin
from apof.menus.models import (
    Meal,
    Menu,
)
from apof.restaurants.models import Restaurant


class BasketTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        self.assertEqual(str(basket), 'Basket christopher')


class OrderTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        meal = Meal(menu=Menu(restaurant=Restaurant(name='restaurant')), name='soup')

        order = Order(basket=basket, meal=meal)
        self.assertEqual(str(order), 'christopher soup')

    def test_get_restaurant(self):
        self.assertEqual(self.order.get_restaurant_name(), 'test restaurant2')

    def test_get_total_price(self):
        expected_total_price = Decimal('26.74')
        self.assertEqual(self.order.get_total_price(), expected_total_price)
