from datetime import datetime

from django.contrib.auth.models import User
from django.test import TestCase
from mock import Mock

from baskets.models import Basket, Order
from menus.models import Meal


class BasketTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='christopher',
            email='christopher@wp.pl',
        )

    def test_string_representation(self):
        basket = Basket(owner=self.user)
        self.assertEqual(str(basket), 'Basket christopher')


class OrderTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='christopher',
            email='christopher@wp.pl',
        )

    def test_string_representation(self):
        basket = Basket(owner=self.user)
        meal = Mock(spec=Meal)
        meal._state = Mock(db=None)
        meal.__unicode__ = Mock(return_value='Pizza')
        order = Order(basket=basket, meal=meal)
        order.created_at = datetime(2010, 1, 1, 12, 15, 15)
        self.assertEqual(str(order), 'christopher Pizza 2010-01-01 12:15:15')
