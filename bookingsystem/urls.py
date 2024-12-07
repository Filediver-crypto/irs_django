from django.urls import path
from . import views

urlpatterns = [
    path('', views.bookingsystem, name='bookingsystem'),
]
