from django.contrib.admin import SimpleListFilter, ListFilter, ModelAdmin
from django.contrib.admin.options import BaseModelAdmin
from django.test import TestCase

from apof.baskets.admin import OrderAdmin, BasketAdmin, RestaurantListFilter
from apof.baskets.tests.utils import OrderTestMixin


class OrderAdminTestCase(TestCase):
    def test_inheritance(self):
        self.assertEqual(
            OrderAdmin.__mro__, (OrderAdmin, ModelAdmin, BaseModelAdmin, object)
        )

    def test_constants(self):
        self.assertEqual(
            OrderAdmin.list_display,
            (
                'status',
                'basket',
                'edited_at',
                'get_order_restaurant_name',
                'get_meal_name',
                'size',
                'get_toppings',
                'get_order_price'
            )
        )
        self.assertEqual(
            OrderAdmin.list_filter,
            ('basket__created_at', 'status', RestaurantListFilter)
        )


class BasketAdminTestCase(TestCase):
    def test_inheritance(self):
        self.assertEqual(
            BasketAdmin.__mro__, (BasketAdmin, ModelAdmin, BaseModelAdmin, object)
        )


class RestaurantListFilterTestCase(OrderTestMixin, TestCase):
    fixtures = ['test_user_data.json']

    def test_inheritance(self):
        self.assertEqual(
            RestaurantListFilter.__mro__,
            (RestaurantListFilter, SimpleListFilter, ListFilter, object)
        )

    def test_admin_restaurant_list(self):
        testFilter = RestaurantListFilter(
            self.data_mock,
            self.data_mock,
            self.data_mock,
            self.data_mock
        )
        data1 = testFilter.lookups(self.data_mock, self.data_mock)
        data2 = testFilter.queryset(self.data_mock, data1)
        self.assertEqual(data1[0][1], 'test restaurant2')
        self.assertEqual(data2[0][1], 'test restaurant2')
