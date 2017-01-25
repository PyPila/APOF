from django.contrib import admin

from .models import (
    Meal,
    MealCategory,
    MealPrice,
    Menu,
    Restaurant,
    Size,
)


class MealPriceInline(admin.TabularInline):
    model = MealPrice

# class SizeInline(admin.StackedInline):
#     model = Size

class MealAdmin(admin.ModelAdmin):
    inlines = [
        MealPriceInline
    ]
    list_display = ('name', 'prices')

    def prices(self, obj):
        return ','.join([price.value for price in obj.mealprice_set.all()])

class MealCategoryAdmin(admin.ModelAdmin):
    pass

class MealPriceAdmin(admin.ModelAdmin):
    pass

class MenuAdmin(admin.ModelAdmin):
    pass

class RestaurantAdmin(admin.ModelAdmin):
    pass

class SizeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Meal, MealAdmin)
admin.site.register(MealCategory, MealCategoryAdmin)
admin.site.register(MealPrice, MealPriceAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Size, SizeAdmin)
