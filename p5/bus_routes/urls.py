# bus_routes/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_interface, name='index'),
]
