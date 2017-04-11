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
