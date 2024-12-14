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
        return f'USER{next_number:03d}'

class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date = models.DateField()
    time_slot = models.CharField(max_length=10)
    room_type = models.CharField(max_length=20)
    building = models.CharField(max_length=50)
    group_size = models.IntegerField()
    purpose = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.room_type} - {self.date} - {self.time_slot}"

