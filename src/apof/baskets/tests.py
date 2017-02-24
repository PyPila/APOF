from decimal import Decimal

from django.contrib.auth.models import Permission, User
from django.core.files import File
from django.shortcuts import reverse
from django.test import TestCase
from mock import MagicMock, patch

from baskets.models import Basket, Order
from baskets.templatetags.get_item import get_item
from baskets.views import OrderListView
from menus.models import (
    Ingredient,
    Meal,
    Menu,
    Price,
    Size,
    Topping
)
from restaurants.models import Restaurant


class BasketTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        self.assertEqual(str(basket), 'Basket christopher')


class OrderTestMixin(TestCase):
    fixtures = ['test_user_data.json']

    @patch('django.core.files.storage.default_storage._wrapped')
    def setUp(self, mocked_storage):
        file_mock = MagicMock(spec=File, name='FileMock')
        file_mock.name = 'test1.jpg'
        restaurant = Restaurant.objects.create(name='test restaurant2', logo=file_mock)
        menu = Menu.objects.create(restaurant=restaurant)
        size = Size.objects.create(menu=menu, value=15, value_unit='cm')
        test_meal = Meal.objects.create(menu=menu, name='test_meal')
        test1_topping = Topping.objects.create(
            menu=menu,
            ingredient=Ingredient.objects.create(
                name='test1_ingredient'
            )
        )
        test2_topping = Topping.objects.create(
            menu=menu,
            ingredient=Ingredient.objects.create(
                name='test2_ingredient'
            )
        )
        Price.objects.bulk_create([
            Price(value=22.99, size=size, content_object=test_meal),
            Price(value=2.5, size=size, content_object=test1_topping),
            Price(value=1.25, size=size, content_object=test2_topping)
        ])

        self.order = Order.objects.create(
            basket=Basket.objects.create(owner=User.objects.get(username='christopher')),
            meal=test_meal,
            size=size
        )
        self.order.toppings.set([test1_topping, test2_topping])


class OrderTestCase(OrderTestMixin):

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


class OrderListViewTestCase(OrderTestMixin):

    def test_constants(self):
        self.assertEqual(OrderListView.model, Order)
        self.assertEqual(OrderListView.permission_required, ('baskets.delete_order', ))
        self.assertTrue(OrderListView.raise_exception)
        self.assertEqual(OrderListView.ordering, ('meal__menu__restaurant', ))

    def test_anonymous_user_gets_304(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_without_permission_gets_304(self):
        self.client.force_login(User.objects.get(username='christopher'))
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_with_permission(self):
        user = User.objects.get(username='christopher')
        user.user_permissions.add(Permission.objects.get(codename='delete_order'))
        self.client.force_login(user)
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)


class OrderDeleteViewTestCase(OrderTestMixin):

    def test_constants(self):
        self.assertEqual(OrderListView.model, Order)
        self.assertEqual(OrderListView.permission_required, ('baskets.delete_order', ))
        self.assertEqual(OrderListView.ordering, ('meal__menu__restaurant', ))

    def test_anonymous_user_gets_304(self):
        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_without_permission_gets_304(self):
        self.client.force_login(User.objects.get(username='christopher'))
        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logger_user_with_permission(self):
        user = User.objects.get(username='christopher')
        user.user_permissions.add(Permission.objects.get(codename='delete_order'))
        self.client.force_login(user)
        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 200)


class GetItemTagTestCase(TestCase):

    def test_get_item(self):
        test_dict = {'a': 1, '2': 'b'}
        self.assertEqual(get_item(test_dict, 'a'), 1)
        self.assertIsNone(get_item(test_dict, 'b'))
