from django.conf.urls import include, url
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='home'),
    url(
        r'^login/$',
        auth_views.login,
        {'redirect_authenticated_user': True},
        name='login'
    ),
    url(
        r'^logout/$',
        auth_views.logout,
        {'next_page': '/portal'},
        name='logout'
    ),
]
