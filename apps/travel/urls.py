from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.welcome),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add_page),
    url(r'^travels/add/add_trip$', views.add_trip),
    url(r'^travels/destination/(?P<trip_id>\d+)$', views.show),
    url(r'^travels/destination/delete/(?P<trip_id>\d+)$', views.delete_trip),
    url(r'^travels/join/(?P<trip_id>\d+)$', views.join),
    url(r'^travels/unjoin/(?P<trip_id>\d+)$', views.unjoin)
]
