from django.conf.urls import url

from apof.baskets import views


urlpatterns = [
    url(r'^$', views.UserBasketView.as_view(), name='basket'),
    url(
        r'^add/(?P<meal_id>[0-9]+)/(?P<meal_price_id>[0-9]+)/$',
        views.add_meal_to_basket,
        name='add-meal-to-basket'
    ),
    url(r'^del/(?P<pk>[0-9]+)/delete$', views.OrderDeleteUserView.as_view(), name='user-order-delete'),
    url(r'^orders/$', views.OrderListView.as_view(), name='order-list'),
    url(
        r'^orders/(?P<pk>[0-9]+)/delete',
        views.OrderDeleteView.as_view(),
        name='order-delete'
    )
]
