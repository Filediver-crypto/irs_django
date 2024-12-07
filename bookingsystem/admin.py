from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('name', 'date', 'time_slot', 'room_type', 'building', 'student_id')
    list_filter = ('date', 'room_type', 'building')
    search_fields = ('name', 'student_id', 'email')
    ordering = ('-date', 'time_slot')


