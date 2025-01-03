from django.contrib import admin
from .models import Booking, CustomUser, Room

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'date', 'start_time', 'end_time', 'building', 'group_size', 'purpose')
    list_filter = ('date', 'room_type', 'building')
    search_fields = ('room_type', 'building', 'purpose')
    ordering = ('-date', 'start_time')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'user_email', 'is_professor')
    list_filter = ('is_professor',)
    search_fields = ('username', 'user_id', 'user_email')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    search_fields = ('name', 'size')