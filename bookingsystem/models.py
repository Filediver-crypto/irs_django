from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    user_id = models.CharField(max_length=20, unique=True)
    user_email = models.EmailField(unique=True)
    is_professor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.username} ({self.user_id})"

    @classmethod
    def generate_user_id(cls):
        # Get the last user
        last_user = cls.objects.order_by('-user_id').first()
        
        if last_user and last_user.user_id.startswith('USER'):
            # Extract the number and increment it
            try:
                last_number = int(last_user.user_id[4:])  # Skip 'USER' prefix
                next_number = last_number + 1
            except ValueError:
                next_number = 1
        else:
            next_number = 1
            
        # Format: USER001, USER002, etc.
        return f'{next_number:03d}'

class Room(models.Model):
    room_id = models.IntegerField(default=1)
    name = models.CharField(max_length=100)  # Name of the room
    size = models.IntegerField()  # Maximum number of people
    building = models.CharField(max_length=100, default = "a")  # Building of the Room
    isworkroom = models.BooleanField(default=False)
    utility = models.TextField(blank=True, null=True)  # Optional description
    #BUILDING_CHOICES = [
    #    ('MAIN', 'Main Building'),
    #    ('SCIENCE', 'Science Building'),
    #    ('ARTS', 'Arts Building'),
    #    ('LIBRARY', 'Library'),
    #]
    building = models.TextField(blank=True, null=True)
                                #max_length=20, choices=BUILDING_CHOICES, default='A')

    def __str__(self):
        return f"{self.name} - {self.size} - {self.isworkroom} - {self.utility}"

class Course(models.Model):
    name = models.CharField(max_length=100) 
    dozent = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    students = models.ManyToManyField(CustomUser, related_name='courses')
    
    
    def __str__(self):
        return f"{self.name} - {self.dozent} - {self.students.count()} students"


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField()  # New field for start time
    end_time = models.TimeField()    # New field for end time
    room_id = models.ForeignKey(Room, on_delete=models.CASCADE, default=1)
    room_type = models.CharField(max_length=20)
    building = models.CharField(max_length=50)
    group_size = models.IntegerField()
    purpose = models.CharField(max_length=50)
    course = models.ForeignKey('Course', null=True, blank=True, on_delete=models.SET_NULL)
    #For the Fullcalendar format
    title = f"{room.name} ({purpose})"
    start = f"{date}T{start_time}"
    end = f"{date}T{end_time}"


    def __str__(self):
        if self.course:
            return f"Course Booking: {self.course.name} on {self.date} ({self.start_time} - {self.end_time})"
        return f"{self.room_type} - {self.room.name} - {self.date} - {self.start_time} - {self.end_time}"

    

    