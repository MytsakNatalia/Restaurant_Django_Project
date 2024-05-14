from django.test import TestCase
from django.urls import reverse, resolve
from reservations.views import *
from users.models import User

class TestUrlsReservations(TestCase):
    def setUp(self):
        # Create a User
        self.user = User.objects.create(username='test_user')

        # Create a Table
        self.table = Table.objects.create(max_number=4)

        # Create a Reservation for testing
        now = timezone.now()
        self.reservation = Reservation.objects.create(
            user=self.user,
            table=self.table,
            time=now + timedelta(days=2),  
            status=False
        )  
    
    def test_book_table_resolved(self):
        url = reverse('reservations:booktbl')
        self.assertEquals(resolve(url).func, booktbl)
        
    def test_my_reservations_reselved(self):
        url = reverse('reservations:user_reservations')
        self.assertEquals(resolve(url).func, user_reservations)

    def test_cancel_reservation_resolved(self):
        url = reverse('reservations:cancel_reservation', args=[self.reservation.id])
        self.assertEquals(resolve(url).func, cancel_reservation)