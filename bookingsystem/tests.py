from django.test import TestCase
from models import Booking, Room

def room_booking_data():
    room_id = Room.room_id('1')

    
    if room_id:
        bookings = Booking.objects.filter(room_id=room_id)
    else:
        bookings = []

    print(bookings)
