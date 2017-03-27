from django.contrib.auth.models import User
from django.core.files import File
from django.shortcuts import reverse
from django.test import TestCase
from mock import MagicMock, patch

from baskets.models import Basket, Order
from menus.models import (
    Meal,
    Menu,
    Price,
    Size
)
from restaurants.models import Restaurant


class BasketTest(TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))

        self.assertEqual(str(basket), 'Basket christopher')


class OrderTest(TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        meal = Meal(menu=Menu(restaurant=Restaurant(name='restaurant')), name='soup')
        order = Order(basket=basket, meal=meal)

        self.assertEqual(str(order), 'christopher soup')


class AddToBasketViewTestCase(TestCase):
    fixtures = ['test_user_data.json']

    @patch('django.core.files.storage.default_storage._wrapped')
    def setUp(self, mocked_storage):
        self.user = User.objects.get(username='christopher')
        file_mock = MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        menu = Menu.objects.create(restaurant=restaurant)
        self.size = Size.objects.create(menu=menu, value=15, value_unit='cm')
        self.meal = Meal.objects.create(menu=menu, name='test_meal')
        self.price = Price.objects.create(value=22.99, size=self.size, content_object=self.meal)

    def _get_url(self, meal, price):
        url = reverse(
            'add-meal-to-basket',
            kwargs={
                'meal_id': meal.id,
                'meal_price_id': price.id
            }
        )
        return url

    def test_anonymous_user_is_redirected_to_login_view(self):
        response = self.client.get(self._get_url(self.meal, self.price))

        self.assertRedirects(
            response,
            '{}{}{}'.format(
                reverse('login'),
                '?next=',
                self._get_url(self.meal, self.price)
            )
        )

    def test_logged_user_can_create_order_with_meal_in_basket(self):
        self.client.force_login(self.user)
        response = self.client.get(self._get_url(self.meal, self.price))
        order = Order.objects.get(pk=1)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.all().count(), 1)
        self.assertEqual(order.basket.owner, self.user)
        self.assertEqual(order.meal, self.meal)
        self.assertEqual(order.size, self.size)

    def test_logged_user_is_redirected_after_creating_order(self):
        self.client.force_login(self.user)
        expected_url = reverse('meal-list', kwargs={'restaurant_pk': 1})
        response = self.client.get(
            self._get_url(
                self.meal,
                self.price
            ),
            HTTP_REFERER=expected_url
        )

        self.assertRedirects(response, expected_url)
