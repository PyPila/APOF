from django.contrib import admin

from .models import Basket, Order


class OrderAdmin(admin.ModelAdmin):
    list_display = ('status', 'basket', 'meal')


class BasketAdmin(admin.ModelAdmin):
    list_display = ('owner', 'created_at')


admin.site.register(Basket, BasketAdmin)
admin.site.register(Order, OrderAdmin)
