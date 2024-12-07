from django.db import models

class Booking(models.Model):
    date = models.DateField()
    time_slot = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20)
    building = models.CharField(max_length=20)
    group_size = models.IntegerField()  
    student_id = models.CharField(max_length=20)
    name = models.CharField(max_length=20)
    email = models.EmailField()
    purpose = models.CharField(max_length=20)

