from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase

from menus.models import (
    Ingredient,
    Meal,
    Menu,
    Price,
    Size,
    Topping
)
from restaurants.models import Restaurant


class MenuTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test restaurant'
        menu = Menu(restaurant=Restaurant(name=expected_result))
        self.assertEqual(str(menu), expected_result)


class SizeTestCase(TestCase):

    def test_string_representation_returns_default_if_desc_and_value_is_empty(self):
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        size = Size(menu=menu)
        expected_result = 'Normal size'
        self.assertEqual(str(size), expected_result)

    def test_string_representation_if_description_value_and_value_unit_provided(self):
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        size = Size(menu=menu, description='Test size', value='32', value_unit='cm')
        expected_result = 'Test size (32 cm)'
        self.assertEqual(str(size), expected_result)


class MealTestCase(TestCase):

    def test_string_representation(self):
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        meal = Meal(menu=menu, name='test meal')
        expected_result = 'test restaurant | test meal'
        self.assertEqual(str(meal), expected_result)


class ToppingTestCase(TestCase):

    def test_string_representation(self):
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        ingredient = Ingredient(name='test ingredient')
        topping = Topping(menu=menu, ingredient=ingredient)
        expected_result = 'test restaurant | test ingredient'
        self.assertEqual(str(topping), expected_result)


class IngredientTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test ingredient'
        ingredient = Ingredient(name=expected_result)
        self.assertEqual(str(ingredient), expected_result)


class PriceTestCase(TestCase):

    def test_string_representation(self):
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        size = Size(menu=menu, description='Test size', value='32', value_unit='cm')
        meal = Meal(menu=menu, name='test meal')
        price = Price(value='24.99', size=size, content_object=meal)
        expected_result = '24.99'
        self.assertEqual(str(price), expected_result)


class MealListViewTestCase(TestCase):
    fixtures = ['test_user_data.json']

    def setUp(self):
        self.user = User.objects.get(username='christopher')

    def test_anonymous_user_is_redirected_to_login_view(self):
        response = self.client.get(reverse('meal-list', kwargs={'restaurant_pk': 1}))
        redirect_url = '{}{}{}'.format(
            reverse('login'),
            '?next=',
            reverse(
                'meal-list',
                kwargs={'restaurant_pk': 1}
            )
        )
        self.assertRedirects(response, redirect_url)

    def test_logged_user_is_not_redirected(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('meal-list', kwargs={'restaurant_pk': 1}))
        self.assertEqual(response.status_code, 200)
