
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking, Room
import json

#LOGIN AND REGISTER

def login_register(request):
    return render(request, 'auth/login_register.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'auth/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'auth/login.html', {'form': form})



#BOOKINGSYSTEM

def bookingsystem(request):
    # Time selection (hours and minutes)
    hours = range(8, 19)  # Hours from 8 AM to 6 PM
    minutes = range(0, 60, 5)  # Minutes from 00 to 55 in 5-minute intervals
    
    # Handle form submission
    if request.method == 'POST':
        try:
            # Create a new booking object with current user and form data
            booking = Booking(
                user=request.user,
                date=request.POST['date'],
                start_time=request.POST['start_time'],
                end_time=request.POST['end_time'],
                room_type=request.POST['room_type'],
                building=request.POST['building'],
                group_size=int(request.POST['group_size']),
                purpose=request.POST['purpose']
            )
            booking.save()
            return redirect('dashboard')  # Redirect to a dashboard or success page
        except Exception as e:
            print(f"Booking error: {e}")
            return render(request, 'bookingsystem.html', {
                'error': 'Booking failed. Please try again.',
                'hours': hours,
                'minutes': minutes
            })
 # If it's a GET request, just render the booking form with the time selection options
    return render(request, 'bookingsystem.html', {
        'hours': hours,
        'minutes': minutes
    })



#DASHBOARD

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



#MY BOOKINGS

@login_required
def my_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    
    return render(request, 'my_bookings.html', {'bookings': user_bookings})


@login_required
def user_bookings_api(request):
    user = request.user
    bookings = Booking.objects.filter(user=user)
    events = [
        {
            "id": b.id,
            "calendarId": "1",
            "title": f"Booking: {b.room.name}",
            "category": "time",
            "start": b.start_date.isoformat(),
            "end": b.end_date.isoformat(),
        }
        for b in bookings
    ]
    return JsonResponse(events, safe=False)


#ROOMPLAN

@login_required
def roomplan(request):   
    return render(request, 'roomplan_detail.html')



