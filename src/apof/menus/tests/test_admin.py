from django.contrib.admin import ModelAdmin
from django.contrib.admin.options import InlineModelAdmin, BaseModelAdmin
from django.contrib.contenttypes.admin import (
    GenericTabularInline,
    GenericInlineModelAdmin
)
from django.test import TestCase

from apof.menus.admin import (
    PriceInline,
    MealAdmin,
    ToppingAdmin,
    SizeAdmin
)


class AdminTestCase(TestCase):

    def test_price_in_line(self):
        expectedMRO = (
            PriceInline,
            GenericTabularInline,
            GenericInlineModelAdmin,
            InlineModelAdmin,
            BaseModelAdmin,
            object
        )
        self.assertEqual(PriceInline.__mro__, expectedMRO)

    def test_meal_admin(self):
        self.assertEqual(
            MealAdmin.__mro__,
            (MealAdmin, ModelAdmin, BaseModelAdmin, object)
        )

    def test_topping_admin(self):
        self.assertEqual(
            ToppingAdmin.__mro__,
            (ToppingAdmin, ModelAdmin, BaseModelAdmin, object)
        )

    def test_size_admin(self):
        self.assertEqual(
            SizeAdmin.__mro__,
            (SizeAdmin, ModelAdmin, BaseModelAdmin, object)
        )
