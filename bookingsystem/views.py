
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking, Room
from django.db.models import Q
from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
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

@login_required
def bookingsystem(request):
    # Time selection (hours and minutes)
    hours = range(8, 19)  # Hours from 8 AM to 6 PM
    minutes = range(0, 60, 5)  # Minutes from 00 to 55 in 5-minute intervals

    listofpossiblerooms = []

    tempdate=None
    tempstart_time=None
    tempend_time=None
    temproom_type=None
    tempbuilding=None
    tempgroup_size=None
    temppurpose=None
    
    # Handle form submission
    if request.method == 'POST':
        try:


            tempdate=request.POST['date']
            tempstart_time=request.POST['start_time']
            tempend_time=request.POST['end_time']
            temproom_type=request.POST['room_type']
            tempbuilding=request.POST['building']
            tempgroup_size=int(request.POST['group_size'])
            temppurpose=request.POST['purpose']


            
            

            if temproom_type == "individual" :

                possiblerooms = Room.objects.filter(building=tempbuilding, size__gte=tempgroup_size, isworkroom =False) 

                

                #Algorythem if the room is free in this Time


                bookingpossible = True

                print("Ist das hier zu sehen")
                print(tempbuilding)
                print(tempgroup_size)
                print(possiblerooms)
                
                for room in possiblerooms:
                    buchungen = Booking.objects.filter(room_id=room.room_id)
                    
                    print("Raum" + str(room.room_id) + " wird untersucht")

                    bookingpossible = True

                    for buchung in buchungen:
                        
                        if bookingpossible == True :

                            if str(buchung.start_time) < str(tempstart_time) <= str(buchung.end_time) :
                                if str(buchung.start_time) <= str(tempend_time) < str(buchung.end_time):
                                    bookingpossible = True
                                else :
                                    bookingpossible = False
                            else:
                                bookingpossible = False
                                
                        else :
                            break

                    
                    if bookingpossible == True :
                        listofpossiblerooms.append(room.room_id)


            elif temproom_type == "sharedroom":

                #Algorythem if in the Rooms seats are Emty

                possiblerooms = Room.objects.filter(building=tempbuilding, size__gte=tempgroup_size, isworkroom =True) 


                bookingpossible = True

                
                for room in possiblerooms:
                    buchungen = Booking.objects.filter(room_id=room.room_id)
                    
                    
                    step = str(timedelta(minutes=5))

                    # Iteration von starttime bis endtime
                    current_time = tempstart_time
                    while current_time <= tempend_time:

                        peopleinroom = 0

                        for buchung in buchungen:

                            buchungssize = buchung.group_size 

                            if buchung.start_time <= current_time < buchung.end_time :
                                    peopleinroom = peopleinroom + buchungssize
                                    
                            
                        if not peopleinroom <= room.size :
                            bookingpossible = False
                            break
                          
                        current_time += step
                    



   
                    if bookingpossible == True :
                        listofpossiblerooms.append(room.room_id)
            
            print(listofpossiblerooms)

            request.session['tempdata'] = {
            'date': tempdate,
            'start_time': tempstart_time,
            'end_time': tempend_time,
            'room_type': temproom_type,
            'building': tempbuilding,
            'group_size': tempgroup_size,
            'purpose': temppurpose,
        }

            request.session['listofpossiblerooms'] = listofpossiblerooms


            request.session.save()

            

            return redirect('booking_suggestion')  # Redirect to a dashboard or success page
        

        except Exception as e:
                    print(f"Booking error: {e}")
                    return render(request, 'bookingsystem.html', {
                        'error': 'Booking failed. Please try again.',
                        'hours': hours,
                        'minutes': minutes
                    })       

    return render(request, 'bookingsystem.html', {
        'hours': hours,
        'minutes': minutes
    })      

#Booking suggestion   
  
@login_required
def booking_suggestion(request):
    # Session-Daten abrufen
    tempdata = request.session.get('tempdata', {})
    listofpossiblerooms = request.session.get('listofpossiblerooms', [])

    if not listofpossiblerooms:
        return render(request, 'booking_suggestion.html', {
            'error': 'Keine verfügbaren Räume gefunden.',
            'options': []
        })

    # Erster Raumvorschlag
    suggested_room_id = listofpossiblerooms[0]
    suggested_room = Room.objects.get(id=suggested_room_id)
    suggested_room_name = suggested_room.name

    # Dropdown-Optionen: Abrufen der Room-Objekte
    options = Room.objects.filter(id__in=listofpossiblerooms[1:])

    if request.method == 'POST':
        action = request.POST.get('action')
        selected_option = request.POST.get('selected_option')

        if action == 'accept_suggestion':
            # Buchung für den vorgeschlagenen Raum
            booking = Booking(
                user=request.user,
                date=tempdata['date'],
                start_time=tempdata['start_time'],
                end_time=tempdata['end_time'],
                room_type=tempdata['room_type'],
                building=tempdata['building'],
                group_size=tempdata['group_size'],
                purpose=tempdata['purpose'],
                room_id=suggested_room  # Hier wird die Room-Instanz verwendet
            )
            booking.save()
            return redirect('my_bookings')

        elif action == 'accept_dropdown' and selected_option:
            # Buchung für die Auswahl aus dem Dropdown
            room = Room.objects.get(id=selected_option)

            booking = Booking(
                user=request.user,
                date=tempdata['date'],
                start_time=tempdata['start_time'],
                end_time=tempdata['end_time'],
                room_type=tempdata['room_type'],
                building=tempdata['building'],
                group_size=tempdata['group_size'],
                purpose=tempdata['purpose'],
                room_id=room  # Hier wird die Room-Instanz verwendet
            )
            booking.save()
            return redirect('my_bookings')

    return render(request, 'booking_suggestion.html', {
        'suggested_room_name': suggested_room_name,
        'options': options
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



