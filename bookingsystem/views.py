
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking, Room, Course
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
    
    # Fetch all courses for professors to select from
    courses = Course.objects.all()

    # Handle form submission
    if request.method == 'POST':
        try:
            # Extract form data
            date = request.POST['date']
            start_time = request.POST['start_time']
            end_time = request.POST['end_time']
            room_type = request.POST['room_type']
            building = request.POST['building']
            group_size = int(request.POST['group_size'])
            purpose = request.POST['purpose']
            course_id = request.POST.get('course')  # Optional course ID
            
            # Check if the user is a professor and a course is selected
            if request.user.is_professor and course_id:
                course = Course.objects.get(id=course_id)

                # Create a booking for the professor
                booking = Booking.objects.create(
                    user=request.user,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    room_type=room_type,
                    building=building,
                    group_size=course.students.count(),  # Group size = total students in course
                    purpose=f"Course: {course.name}",
                    course=course
                )

                # Create bookings for all students in the course
                for student in course.students.all():
                    Booking.objects.create(
                        user=student,
                        date=date,
                        start_time=start_time,
                        end_time=end_time,
                        room_type=room_type,
                        building=building,
                        group_size=1,
                        purpose=f"Course: {course.name}",
                        course=course
                    )
            else:
                # Create a standard booking for the user
                booking = Booking.objects.create(
                    user=request.user,
                    date=date,
                    start_time=start_time,
                    end_time=end_time,
                    room_type=room_type,
                    building=building,
                    group_size=group_size,
                    purpose=purpose
                )
            
            return redirect('dashboard')  # Redirect to a dashboard or success page

        except Exception as e:
            print(f"Booking error: {e}")
            return render(request, 'bookingsystem.html', {
                'error': 'Booking failed. Please try again.',
                'hours': hours,
                'minutes': minutes,
                'courses': courses
            })

    # If it's a GET request, render the booking form with the time selection options and courses
    return render(request, 'bookingsystem.html', {
        'hours': hours,
        'minutes': minutes,
        'courses': courses
    })




#DASHBOARD

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')



#MY BOOKINGS


@login_required
def my_bookings(request):

    user_bookings = Booking.objects.filter(user=request.user).order_by('date', 'start_time')
    return render(request, 'my_bookings.html', {'bookings': user_bookings})


@login_required
def user_booking_data(request):
    # Provide JSON data for FullCalendar
    user_bookings = Booking.objects.filter(user=request.user)

    events = []
    for booking in user_bookings:
        events.append({
            "id": booking.id,
            "title": f"{booking.room_type} ({booking.purpose})",
            "start": f"{booking.date}T{booking.start_time}",
            "end": f"{booking.date}T{booking.end_time}",
            "allDay": False,
        })

    return JsonResponse(events, safe=False)



#ROOMPLAN

@login_required
def room_plans(request):
    # Get all rooms for the dropdown menu
    rooms = Room.objects.all()

    # Get the selected room from the request (default to the first room)
    selected_room_id = request.GET.get('room_id', rooms.first().id if rooms else None)

    # Pass the rooms and selected room to the template
    context = {
        'rooms': rooms,
        'selected_room_id': int(selected_room_id) if selected_room_id else None,
    }
    return render(request, 'room_plans.html', context)


@login_required
def room_booking_data(request):
    # Get the room ID from the request parameters
    room_id = request.GET.get('room_id')

    # Fetch all bookings for the selected room
    if room_id:
        bookings = Booking.objects.filter(room_id=room_id)
    else:
        bookings = []

    # Format data for FullCalendar
    events = []
    for booking in bookings:
        events.append({
            "id": booking.id,
            "title": f"{booking.room_type} ({booking.purpose})",
            "start": f"{booking.date}T{booking.start_time}",
            "end": f"{booking.date}T{booking.end_time}",
            "allDay": False,
        })

    return JsonResponse(events, safe=False)



