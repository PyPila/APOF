from django.contrib import admin

from apof.restaurants.models import Restaurant
from .models import Basket, Order


class RestaurantListFilter(admin.SimpleListFilter):
    title = 'restaurant'
    parameter_name = 'restaurant'

    def lookups(self, request, model_admin):
        return Restaurant.objects.values_list('id', 'name')

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(meal__menu__restaurant__id=self.value())
        else:
            return queryset


class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'status',
        'basket',
        'edited_at',
        'get_order_restaurant_name',
        'get_meal_name',
        'size',
        'get_toppings',
        'get_order_price'
    )
    list_filter = ('basket__created_at', 'status', RestaurantListFilter)

    def get_meal_name(self, obj):
        return obj.meal.name
    get_meal_name.short_description = 'Meal'

    def get_order_price(self, obj):
        return obj.get_total_price()
    get_order_price.short_description = 'Price'

    def get_order_restaurant_name(self, obj):
        return obj.get_restaurant_name()
    get_order_restaurant_name.short_description = 'Restaurant'

    def get_toppings(self, obj):
        order_toppings = obj.toppings.values('ingredient__name').all()
        return ', '.join([topping['ingredient__name'] for topping in order_toppings])
    get_toppings.short_description = 'Toppings'


class BasketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at')


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
