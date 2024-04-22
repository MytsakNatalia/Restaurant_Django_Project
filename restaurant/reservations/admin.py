from django.contrib import admin
from reservations.models import Table, Reservation

admin.site.register(Table)
admin.site.register(Reservation)