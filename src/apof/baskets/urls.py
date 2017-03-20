from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^$', views.UserBasketView.as_view(), name='basket')
]
