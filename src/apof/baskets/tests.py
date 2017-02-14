from django.contrib.auth.models import User
from django.test import TestCase

from baskets.models import Basket, Order
from menus.models import Meal, Menu
from restaurants.models import Restaurant


class BasketTest(TestCase):
    fixtures = ['test-user-data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        self.assertEqual(str(basket), 'Basket christopher')


class OrderTest(TestCase):
    fixtures = ['test-user-data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        meal = Meal(menu=Menu(restaurant=Restaurant(name='restaurant')), name='soup')
        order = Order(basket=basket, meal=meal)
        self.assertEqual(str(order), 'christopher soup')
