from django.conf.urls import include, url
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    url(r'', include('social_django.urls', namespace='social')),
    url(r'^$', views.index, name='home'),
    url(r'^logout/$', auth_views.logout, {'next_page': '/portal'}, name='logout'),
    url(r'^login/$', views.login, name='login'),
]
