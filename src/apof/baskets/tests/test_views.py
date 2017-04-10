from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from apof.baskets.models import Order
from apof.baskets.tests.utils import OrderTestMixin
from apof.baskets.views import OrderListView, OrderDeleteView


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
        self.assertEqual(response.status_code, 200)