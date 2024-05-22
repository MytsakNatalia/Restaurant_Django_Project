from django.urls import path, include
from reservations.views import *
app_name = 'reservations'
urlpatterns = [
    path('booktbl/', booktbl, name='booktbl' ),
    path('myreservation/', user_reservations, name='user_reservations'),
    path('cancel_reservation/<int:reservation_id>/', cancel_reservation, name='cancel_reservation'),
]    