from django.shortcuts import render, redirect
from .models import Booking

# Create your views here.
def bookingsystem(request):
    if request.method == 'POST':
        # Create a new booking object with form data
        booking = Booking(
            date=request.POST['date'],
            time_slot=request.POST['time_slot'],
            room_type=request.POST['room_type'],
            building=request.POST['building'],
            group_size=request.POST['group_size'],
            student_id=request.POST['student_id'],
            name=request.POST['name'],
            email=request.POST['email'],
            purpose=request.POST['purpose']
        )
        booking.save()  # Save the booking to the database
        return redirect('bookingsystem')  # Redirect to the same page or a success page

    return render(request, 'bookingsystem.html')