from django.conf.urls import url

from .views import basket_view


urlpatterns = [
    url(r'^$', basket_view, name='basket')
]
