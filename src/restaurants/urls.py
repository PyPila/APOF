from django.conf.urls import url

from .views import restaurants_list

urlpatterns = [
    url(r'^$', restaurants_list, name='restaurant-list')
]