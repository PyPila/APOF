from django.contrib.auth.models import User, Permission
from django.core.files import File
from django.test import TestCase
from django.urls import reverse
from django.utils.timezone import datetime
from mock import MagicMock, patch

from apof.baskets.models import Order, Basket
from apof.baskets.tests.utils import OrderTestMixin
from apof.baskets.views import (
    OrderListView,
    OrderDeleteView,
    UserBasketView,
    UserBasketConfirmationView,
    UserBasketDeleteView,
    UserOrderQuantityUpdateView
)
from apof.menus.models import (
    Meal,
    Menu,
    Price,
    Size,
)
from apof.restaurants.models import Restaurant


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
        self.price = Price.objects.create(
            value=22.99, size=self.size,
            content_object=self.meal
        )
        self.order = Order.objects.create(
            basket=Basket.objects.create(owner=self.user),
            meal=self.meal,
            size=self.size
        )

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
        order = self.order
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Order.objects.all().count(), 2)
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


class OrderListViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(OrderListView.model, Order)
        self.assertEqual(OrderListView.permission_required, ('baskets.delete_order', ))
        self.assertTrue(OrderListView.raise_exception)
        self.assertEqual(OrderListView.ordering, ('meal__menu__restaurant', ))

    def test_anonymous_user_gets_403(self):
        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_without_permission_gets_403(self):
        self.client.force_login(User.objects.get(username='christopher'))

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_with_permission(self):
        user = User.objects.get(username='christopher')
        user.user_permissions.add(Permission.objects.get(codename='delete_order'))
        self.client.force_login(user)

        response = self.client.get(reverse('order-list'))
        self.assertEqual(response.status_code, 200)


class OrderDeleteViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(OrderDeleteView.model, Order)
        self.assertEqual(OrderDeleteView.permission_required, ('baskets.delete_order', ))
        self.assertTrue(OrderDeleteView.raise_exception)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logged_user_without_permission_gets_403(self):
        self.client.force_login(User.objects.get(username='christopher'))

        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 403)

    def test_logger_user_with_permission(self):
        user = User.objects.get(username='christopher')
        user.user_permissions.add(Permission.objects.get(codename='delete_order'))
        self.client.force_login(user)

        response = self.client.get(reverse('order-delete', kwargs={'pk': self.order.pk}))
        self.assertEqual(response.status_code, 302)


class UserBasketViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(UserBasketView.model, Basket)
        self.assertTrue(UserBasketView.raise_exception)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 403)

    def test_logged_user(self):
        self.client.force_login(self.user1)

        response = self.client.get(reverse('basket'))
        self.assertEqual(response.status_code, 200)


class UserBasketConfirmationViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(UserBasketConfirmationView.model, Basket)
        self.assertTrue(UserBasketConfirmationView.raise_exception)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(
            reverse('user-confirm-basket', kwargs={'pk': self.order.basket.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_logged_user(self):
        self.client.force_login(self.user1)
        pk = self.order.basket.pk

        response = self.client.get(
            reverse('user-confirm-basket', kwargs={'pk': pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.user1.basket.values('is_confirmed').get(pk=pk)['is_confirmed']
        )
        self.client.get(
            reverse('user-confirm-basket', kwargs={'pk': pk})
        )
        self.assertFalse(
            self.user1.basket.values('is_confirmed').get(pk=pk)['is_confirmed']
        )

    def test_user_cant_confirm_someone_else_basket(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                'user-confirm-basket',
                kwargs={'pk': self.someone_else_order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cant_confirm_old_basket(self):
        self.client.force_login(self.user1)
        self.order.basket.created_at = datetime(2012, 12, 21, 0, 0, 0, 0)
        self.order.basket.save()

        response = self.client.get(
            reverse(
                'user-confirm-basket',
                kwargs={'pk': self.order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)


class UserBasketDeleteViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(UserBasketDeleteView.model, Basket)
        self.assertTrue(UserBasketDeleteView.raise_exception)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(
            reverse('user-basket-delete', kwargs={'pk': self.order.basket.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_logged_user(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse('user-basket-delete', kwargs={'pk': self.order.basket.pk})
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(0, self.user1.basket.count())

    def test_user_cant_delete_someone_else_basket(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                'user-basket-delete',
                kwargs={'pk': self.someone_else_order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cant_delete_old_basket(self):
        self.client.force_login(self.user1)
        self.order.basket.created_at = datetime(2012, 12, 21, 0, 0, 0, 0)
        self.order.basket.save()

        response = self.client.get(
            reverse(
                'user-basket-delete',
                kwargs={'pk': self.order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)


class UserOrderQuantityUpdateViewTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_constants(self):
        self.assertEqual(UserOrderQuantityUpdateView.model, Order)
        self.assertTrue(UserOrderQuantityUpdateView.raise_exception)

    def test_anonymous_user_gets_403(self):
        response = self.client.get(
            reverse('user-update-quantity', kwargs={'pk': self.order.basket.pk})
        )
        self.assertEqual(response.status_code, 403)

    def test_logged_user(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse('user-update-quantity', kwargs={'pk': self.order.pk})
        )
        self.assertEqual(response.status_code, 302)

    def test_user_cant_delete_someone_else_basket(self):
        self.client.force_login(self.user1)

        response = self.client.get(
            reverse(
                'user-basket-delete',
                kwargs={'pk': self.someone_else_order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)

    def test_user_cant_delete_old_basket(self):
        self.client.force_login(self.user1)
        self.order.basket.created_at = datetime(2012, 12, 21, 0, 0, 0, 0)
        self.order.basket.save()

        response = self.client.get(
            reverse(
                'user-basket-delete',
                kwargs={'pk': self.order.basket.pk}
            )
        )
        self.assertEqual(response.status_code, 404)
