from django.conf.urls import url

from baskets import views

urlpatterns = [
    url(
        r'^add/(?P<meal_id>[0-9]+)/(?P<meal_price_id>[0-9]+)/$',
        views.add_meal_to_basket,
        name='add-meal-to-basket'
    ),
]
