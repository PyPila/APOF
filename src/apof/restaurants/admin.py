from django.contrib import admin

from .models import Restaurant, OpeningHours, PhoneNumber


class OpeningHoursInlineAdmin(admin.TabularInline):
    model = OpeningHours


class PhoneNumberInlineAdmin(admin.TabularInline):
    model = PhoneNumber


class RestaurantAdmin(admin.ModelAdmin):
    inlines = [
        OpeningHoursInlineAdmin,
        PhoneNumberInlineAdmin
    ]


admin.site.register(Restaurant, RestaurantAdmin)
