from django.contrib import admin
from .models import Booking, CustomUser, Room, Course

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'date', 'start_time', 'end_time', 'building', 'group_size', 'purpose',"room_id", 'course')
    list_filter = ('date', 'room_type', 'building','course')
    search_fields = ('room_type', 'building', 'purpose')
    ordering = ('-date', 'start_time')

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'user_id', 'user_email', 'is_professor')
    list_filter = ('is_professor',)
    search_fields = ('username', 'user_id', 'user_email')

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'size', 'building', 'isworkroom')
    search_fields = ('name', 'size', "building")

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'dozent')
    search_fields = ('name', 'dozent')
    filter_horizontal = ('students',)
    