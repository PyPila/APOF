from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase

from baskets.models import Basket, Order
from menus.models import Ingredient, Meal, Menu, Price, Size, Topping
from restaurants.models import Restaurant


class BasketTest(TestCase):
    fixtures = ['test_user_data.json']

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        self.assertEqual(str(basket), 'Basket christopher')


class OrderTest(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        menu = Menu.objects.create(restaurant=Restaurant.objects.create(name='restaurant'))
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

    def test_string_representation(self):
        basket = Basket(owner=User.objects.get(username='christopher'))
        meal = Meal(menu=Menu(restaurant=Restaurant(name='restaurant')), name='soup')
        order = Order(basket=basket, meal=meal)
        self.assertEqual(str(order), 'christopher soup')

    def test_get_restaurant(self):
        self.assertEqual(self.order.get_restaurant_name(), 'restaurant')

    def test_get_total_price(self):
        expected_total_price = Decimal('26.74')
        self.assertEqual(self.order.get_total_price(), expected_total_price)
