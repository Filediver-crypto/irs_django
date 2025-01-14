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
    path('user_booking-data/', views.user_booking_data, name='user_booking-data'),
    path('room_plans/', views.room_plans, name='room_plans'),
    path('room_booking_data/', views.room_booking_data, name='room_booking_data'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking-suggestion/', views.booking_suggestion, name='booking_suggestion'),
]
