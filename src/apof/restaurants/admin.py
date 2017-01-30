from django.contrib import admin

from .models import Restaurant, OpeningHours


class OpeningHoursInlineAdmin(admin.TabularInline):
    model = OpeningHours


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [
        OpeningHoursInlineAdmin,
    ]


admin.site.register(Restaurant, RestaurantAdmin)
