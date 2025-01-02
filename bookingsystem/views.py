from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking, Room

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

@login_required
def bookingsystem(request):
    if request.method == 'POST':
        try:
            # Create a new booking object with current user and form data
            booking = Booking(
                user=request.user,
                date=request.POST['date'],
                time_slot=request.POST['time_slot'],
                room_type=request.POST['room_type'],
                building=request.POST['building'],
                group_size=int(request.POST['group_size']),
                purpose=request.POST['purpose']
            )
            booking.save()
            return redirect('dashboard')
        except Exception as e:
            print(f"Booking error: {e}")
            return render(request, 'bookingsystem.html', {'error': 'Booking failed. Please try again.'})

    return render(request, 'bookingsystem.html')

@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

@login_required
def my_bookings(request):
    user_bookings = Booking.objects.filter(user=request.user)
    return render(request, 'my_bookings.html', {'bookings': user_bookings})

@login_required
def roomplan(request):   
    return render(request, 'roomplan_detail.html')