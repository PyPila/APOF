from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Ingredient,
    Meal,
    Menu,
    Topping,
    Price,
    Restaurant,
    Size,
)


class PriceInline(GenericTabularInline):
    model = Price


class MealAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline
    ]
    list_display = ('name', 'menu',)
    list_filter = ('menu',)


class ToppingAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline
    ]
    list_display = ('ingredient', 'menu')
    list_filter = ('menu',)


class PriceAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass


class MenuAdmin(admin.ModelAdmin):
    pass


class RestaurantAdmin(admin.ModelAdmin):
    pass


class SizeAdmin(admin.ModelAdmin):
    list_display = ('description', 'value', 'value_unit', 'menu')
    list_filter = ('menu',)


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Topping, ToppingAdmin)
