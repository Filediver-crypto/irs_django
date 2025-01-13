from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', views.login_register, name='login_register'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', LogoutView.as_view(next_page='login_register'), name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('booking/', views.bookingsystem, name='bookingsystem'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('roomplan/', views.roomplan, name='roomplan'),
    path('api/my-bookings/', views.user_bookings_api, name='user_bookings_api'),
    path('booking-suggestion/', views.booking_suggestion, name='booking_suggestion'),
]
