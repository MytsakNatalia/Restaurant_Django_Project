from django.db import models
from users.models import User
from datetime import datetime, timedelta
from django.utils import timezone


class Table(models.Model):
    max_number = models.IntegerField()

    def __str__(self):
        return f"Table {self.id}"

class Reservation(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.SET_DEFAULT, default=None)
    table = models.ForeignKey(to=Table, on_delete=models.PROTECT)
    time = models.DateTimeField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"Reservation {self.id}"
            
    def is_cancelable(self):
        now = timezone.now()
        return self.time > now + timedelta(days=1)
    
    def process_reservations():        
        reservations = Reservation.objects.all()
        
        for reservation in reservations:
            if not reservation.is_cancelable():
                reservation.status = True
                reservation.save()