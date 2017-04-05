from django.contrib.admin import ModelAdmin
from django.contrib.auth.models import User
from django.contrib.contenttypes.admin import (
    GenericTabularInline,
    GenericInlineModelAdmin
)
from django.contrib.admin.options import InlineModelAdmin, BaseModelAdmin
from django.test import TestCase
from django.urls import reverse

from menus.admin import (
    PriceInline,
    MealAdmin,
    ToppingAdmin,
    SizeAdmin
)
from menus.models import (
    Category,
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


class AdminTestCase(TestCase):

    def test_price_in_line(self):
        priceinlineMRO = PriceInline.__mro__
        expectedMRO = (
            PriceInline,
            GenericTabularInline,
            GenericInlineModelAdmin,
            InlineModelAdmin,
            BaseModelAdmin,
            object
        )
        self.assertEqual(priceinlineMRO, expectedMRO)

    def test_meal_admin(self):
        mealadminMRO = MealAdmin.__mro__
        expectedMRO = (MealAdmin, ModelAdmin, BaseModelAdmin, object)
        self.assertEqual(mealadminMRO, expectedMRO)

    def test_topping_admin(self):
        toppingadminMRO = ToppingAdmin.__mro__
        expectedMRO = (ToppingAdmin, ModelAdmin, BaseModelAdmin, object)
        self.assertEqual(toppingadminMRO, expectedMRO)

    def test_size_admin(self):
        sizeadminMRO = SizeAdmin.__mro__
        expectedMRO = (SizeAdmin, ModelAdmin, BaseModelAdmin, object)
        self.assertEqual(sizeadminMRO, expectedMRO)
