from django.test import TestCase

from apof.menus.tests.utils import MenusTestMixin
from apof.menus.models import Size


class MenuTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.menu), 'test restaurant')

    def test_repr(self):
        self.assertEqual(repr(self.menu), 'Menu(Restaurant: test restaurant)')


class SizeTestCase(MenusTestMixin, TestCase):

    def test_string_representation_returns_default_if_desc_and_value_is_empty(self):
        self.assertEqual(str(self.size), 'Normal size')

    def test_string_representation_if_description_value_and_value_unit_provided(self):
        size = Size(menu=self.menu, description='Test size', value='32', value_unit='cm')
        self.assertEqual(str(size), 'Test size (32 cm)')

    def test_repr(self):
        self.assertEqual(repr(self.size), 'Size(Menu: test restaurant, Value: None)')


class CategoryTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.category), 'test category')

    def test_repr(self):
        self.assertEqual(repr(self.category), 'Category(Name: test category)')


class MealTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.meal), 'test restaurant | test meal')

    def test_repr(self):
        self.assertEqual(repr(self.meal), 'Meal(Menu: test restaurant, Name: test meal)')


class ToppingTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.topping), 'test restaurant | test ingredient')

    def test_repr(self):
        self.assertEqual(
            repr(self.topping),
            'Topping(Menu: test restaurant, Igredient: test ingredient)'
        )


class IngredientTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.ingredient), 'test ingredient')

    def test_repr(self):
        self.assertEqual(repr(self.ingredient), 'Ingredient(Name: test ingredient)')


class PriceTestCase(MenusTestMixin, TestCase):

    def test_string_representation(self):
        self.assertEqual(str(self.price), '24.99')

    def test_repr(self):
        self.assertEqual(
            repr(self.price),
            'Price(Value: 24.99, Object: test restaurant | test meal)'
        )
