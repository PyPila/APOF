from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline

from .models import (
    Category,
    Ingredient,
    Meal,
    Menu,
    Price,
    Size,
    Topping
)


class PriceInline(GenericTabularInline):
    model = Price


class MealAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline
    ]
    list_display = ('name', 'category', 'menu')
    list_filter = ('menu', )


class ToppingAdmin(admin.ModelAdmin):
    inlines = [
        PriceInline
    ]
    list_display = ('ingredient', 'menu')
    list_filter = ('menu', )


class CategoryAdmin(admin.ModelAdmin):
    pass


class PriceAdmin(admin.ModelAdmin):
    pass


class IngredientAdmin(admin.ModelAdmin):
    pass


class MenuAdmin(admin.ModelAdmin):
    pass


class SizeAdmin(admin.ModelAdmin):
    list_display = ('description', 'value', 'value_unit', 'menu')
    list_filter = ('menu', )


admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Meal, MealAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Price, PriceAdmin)
admin.site.register(Size, SizeAdmin)
admin.site.register(Topping, ToppingAdmin)
