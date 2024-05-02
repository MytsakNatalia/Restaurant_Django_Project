from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from reservations.models import Table, Reservation
from datetime import datetime, timedelta
from django.contrib import messages
from django.utils import timezone

def booktbl(request):
    if request.method == 'POST':       
        num_people = request.POST.get('people')
        date = request.POST.get('date')
        time = request.POST.get('time')
        
        if not num_people or not date or not time:
            messages.error(request, "Please fill in all the fields.")
            return redirect('reservations:booktbl')
    
        datetime_str = f"{date} {time}"
        booking_datetime = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")

        # Check if it's within working hours
        if not is_within_working_hours(booking_datetime):
            messages.error(request, "Sorry, the restaurant is closed during this time.")
            return redirect('reservations:booktbl')

        # Check for available tables
        available_tables = Table.objects.filter(max_number__gte=num_people)
        if available_tables.exists():
            # Book the first available table
            table = available_tables.first()
            reservation = Reservation(user=request.user, table=table, time=booking_datetime)
            reservation.save()
            messages.success(request, "Table booked successfully!")
            return redirect('menu:index')
        else:
            messages.error(request, "Sorry, no tables available for the selected date, time, and number of people.")
            return redirect('reservations:booktbl')
    else:        
        reservations = Reservation.objects.all()
        tables = Table.objects.all()
        context = {
            'title': 'Book Table',
            'reservations': reservations, 
            'tables': tables,
        }
        return render(request, 'reservations/booktbl.html', context)

def is_within_working_hours(datetime_obj):    
    day = datetime_obj.weekday()
    hour = datetime_obj.hour

    if day == 6:  
        return 23 <= hour <= 20
    else:  
        return 10 <= hour <= 22

def user_reservations(request):      
    Reservation.process_reservations()
    user = request.user
    reservations = Reservation.objects.filter(user=user)

    reservation_data = []
    for reservation in reservations:
        reservation_info = {
            'id': reservation.id,
            'date': reservation.time.date(),
            'time': reservation.time.time(),
            'table_id': reservation.table.id,
            'num_people': reservation.table.max_number,
            'status': reservation.status
        }
        reservation_data.append(reservation_info)

    context = {
        'reservations': reservation_data
    }

    return render(request, 'reservations/myreservation.html', context)

def cancel_reservation(request,  reservation_id):    
    reservation = Reservation.objects.get(id=reservation_id)
    reservation.delete() 
          
    return redirect(request.META.get('HTTP_REFERER', 'reservations:user_reservations'))