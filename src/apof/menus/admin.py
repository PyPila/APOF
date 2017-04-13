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


class SizeAdmin(admin.ModelAdmin):
    list_display = ('description', 'value', 'value_unit', 'menu')
    list_filter = ('menu', )


admin.site.register(Category)
admin.site.register(Ingredient)
admin.site.register(Meal, MealAdmin)
admin.site.register(Menu)
admin.site.register(Price)
admin.site.register(Size, SizeAdmin)
admin.site.register(Topping, ToppingAdmin)
