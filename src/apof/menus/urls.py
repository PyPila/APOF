from django.conf.urls import url

from apof.menus import views

urlpatterns = [
    url(r'^(?P<restaurant_pk>[0-9]+)/$', views.MealListView.as_view(), name='meal-list')
]
