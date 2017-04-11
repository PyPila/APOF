from django.test import TestCase

from apof.menus.models import (
    Category,
    Ingredient,
    Meal,
    Menu,
    Price,
    Size,
    Topping
)
from apof.restaurants.models import Restaurant


class MenuTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test restaurant'

        menu = Menu(restaurant=Restaurant(name=expected_result))
        self.assertEqual(str(menu), expected_result)


class SizeTestCase(TestCase):

    def test_string_representation_returns_default_if_desc_and_value_is_empty(self):
        expected_result = 'Normal size'
        menu = Menu(restaurant=Restaurant(name='test restaurant'))

        size = Size(menu=menu)
        self.assertEqual(str(size), expected_result)

    def test_string_representation_if_description_value_and_value_unit_provided(self):
        expected_result = 'Test size (32 cm)'
        menu = Menu(restaurant=Restaurant(name='test restaurant'))

        size = Size(menu=menu, description='Test size', value='32', value_unit='cm')
        self.assertEqual(str(size), expected_result)


class CategoryTestCase(TestCase):

    def test_string_representation(self):
        category_name = 'test category'

        category = Category(name=category_name)
        self.assertEqual(str(category), category_name)


class MealTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test restaurant | test meal'
        menu = Menu(restaurant=Restaurant(name='test restaurant'))

        meal = Meal(menu=menu, name='test meal')
        self.assertEqual(str(meal), expected_result)


class ToppingTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test restaurant | test ingredient'
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        ingredient = Ingredient(name='test ingredient')

        topping = Topping(menu=menu, ingredient=ingredient)
        self.assertEqual(str(topping), expected_result)


class IngredientTestCase(TestCase):

    def test_string_representation(self):
        expected_result = 'test ingredient'

        ingredient = Ingredient(name=expected_result)
        self.assertEqual(str(ingredient), expected_result)


class PriceTestCase(TestCase):

    def test_string_representation(self):
        expected_result = '24.99'
        menu = Menu(restaurant=Restaurant(name='test restaurant'))
        size = Size(menu=menu, description='Test size', value='32', value_unit='cm')
        meal = Meal(menu=menu, name='test meal')

        price = Price(value='24.99', size=size, content_object=meal)
        self.assertEqual(str(price), expected_result)
