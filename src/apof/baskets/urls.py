from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^orders/$', views.OrderListView.as_view(), name='order-list'),
    url(
        r'^orders/(?P<pk>[0-9]+)/delete',
        views.OrderDeleteView.as_view(),
        name='order-delete'
    )
]
