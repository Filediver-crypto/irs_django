
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from .models import Booking, Room
from django.db.models import Q
from datetime import datetime, timedelta
<<<<<<< Updated upstream
=======
from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream

=======
    listofpossiblerooms = []

    tempdate=None
    tempstart_time=None
    tempend_time=None
    temproom_type=None
    tempbuilding=None
    tempgroup_size=None
    temppurpose=None
>>>>>>> Stashed changes
    
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
                
                possiblerooms = Room.objects.filter(Q(building=tempbuilding) & Q(capacity__lte=tempgroup_size))

                #Algorythem if the room is free in this Time


<<<<<<< Updated upstream
                listofrooms = None

            elif temproom_type == "sharedroom":

                possiblerooms = Room.objects.filter(Q(building=tempbuilding) & Q(capacity__lte=tempgroup_size))

                #Algorythem if in the Rooms seats are Emty

                for rooms in possiblerooms:
                    
                    buchungen = Booking.objects.filter(roomid=rooms.room_id)

                    for start, end, anzahl in buchungen:
                    # Wenn die Buchung im angegebenen Zeitraum liegt
                        if start < tempend_time and end > tempstart_time:
                            # Setze die Buchungszeiten auf den Zeitraumbeginn bzw. -ende
                            start = max(start, tempstart_time)
                            end = min(end, tempend_time)
                            
                            # Gehe durch den Zeitraum und zähle die Personen für alle 5-Minuten-Abschnitte
                            current_time = start
                            while current_time < end:
                                if current_time not in tempgroup_size:
                                    tempgroup_size[current_time] = 0
                                tempgroup_size[current_time] += anzahl
                                current_time += timedelta(minutes=5)

                    # Überprüfe, ob irgendwo die Kapazität überschritten wird
                    for time, anzahl_personen in tempgroup_size.items():
                        if anzahl_personen > rooms.size:
                            print(f"Kapazität überschritten bei {time.strftime('%H:%M')}: {anzahl_personen} Personen!")
                            return False

                    print("Kapazität wurde im angegebenen Zeitraum nie überschritten.")
                    return True

                listofrooms = None
            else :
                return None






=======
                bookingpossible = True

                
                
                for room in possiblerooms:
                    buchungen = Booking.objects.filter(roomid=room.room_id)
                    
                    bookingpossible = True

                    for buchung in buchungen:
                        
                        if bookingpossible == True :

                            if buchung.start_time < tempstart_time <= buchung.end_time :
                                if buchung.start_time <= tempend_time < buchung.end_time:
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

                possiblerooms = Room.objects.filter(Q(building=tempbuilding) & Q(capacity__lte=tempgroup_size))


                bookingpossible = True

                
                
                for room in possiblerooms:
                    buchungen = Booking.objects.filter(roomid=room.room_id)
                    
                    
                    step = timedelta(minutes=5)

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


            return redirect('booking_suggestion')  # Redirect to a dashboard or success page
        

        except Exception as e:
                    print(f"Booking error: {e}")
                    return render(request, 'bookingsystem.html', {
                        'error': 'Booking failed. Please try again.',
                        'hours': hours,
                        'minutes': minutes
                    })       

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

    return render(request, 'bookingsystem.html', {
        'hours': hours,
        'minutes': minutes
    })           


"""
>>>>>>> Stashed changes
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

            
 # If it's a GET request, just render the booking form with the time selection options
    return render(request, 'bookingsystem.html', {
        'hours': hours,
        'minutes': minutes
    })
"""

#BOOKING suggestion
@login_required
def booking_suggestion(request):

<<<<<<< Updated upstream
#BOOKING suggestion
@login_required
def booking_suggestion(request):
    return render(request, 'booking_suggestion.html')
=======

    tempdata = request.session.get('tempdata', {})  # Standardwert ist {} falls keine Daten vorhanden sind
    listofpossiblerooms = request.session.get('listofpossiblerooms', [])  # Abrufen der Buchungen, Standardwert ist eine leere Liste
    
    suggested_room_id = listofpossiblerooms.pop[0]


    suggested_room= get_object_or_404(Room, id=suggested_room_id)

    suggested_room_name = suggested_room.name

    dropdown_rooms = listofpossiblerooms[1:]

    tempdate = tempdata.get('date', '')  # Datum
    tempstart_time = tempdata.get('start_time', '')  # Startzeit
    tempend_time = tempdata.get('end_time', '')  # Endzeit
    temproom_type = tempdata.get('room_type', '')  # Raumtyp
    tempbuilding = tempdata.get('building', '')  # Gebäude
    tempgroup_size = tempdata.get('group_size', 0)  # Gruppengröße (mit Defaultwert 0)
    temppurpose = tempdata.get('purpose', '')  # Zweck

    

    options = dropdown_rooms

    textforbutton = f"Der Raum {suggested_room_name} passt am Besten "
    
    if request.method == "POST2":
        booking = Booking(
                user=request.user,
                date=tempdate,
                start_time=tempstart_time,
                end_time=tempend_time,
                room_type=temproom_type,
                building=tempbuilding,
                group_size=tempgroup_size,
                purpose=temppurpose
            )
        booking.save()
        return redirect('my_bookings')

    if request.method == 'POST':
        # Das ausgewählte Item wird durch den POST-Request erhalten
        selected_item = request.POST.get('selected_option', None)
        
        # Hier kannst du das ausgewählte Item weiterverarbeiten (z.B. in der Datenbank speichern oder eine Antwort anzeigen)
        if selected_item:
            # Zum Beispiel: Rückmeldung an den Benutzer
            context = {'message': f"Du hast {selected_item} ausgewählt!"}
            return render(request, 'booking_suggestion.html', context)


    



    # Wenn der POST-Request nicht vorliegt, wird das Dropdown angezeigt
    return render(request, 'booking_suggestion.html', {'options': options})
>>>>>>> Stashed changes

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



