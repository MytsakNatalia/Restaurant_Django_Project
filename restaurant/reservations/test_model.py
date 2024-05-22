from django.test import TestCase
from reservations.models import *


class TableModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Table.objects.create(max_number=2)

    def test_str_method(self):
        table = Table.objects.get(id=1)
        expected_object_name = f'Table {table.id}'
        self.assertEquals(expected_object_name, f'Table {table.id}')

    def test_max_number_content(self):
        table = Table.objects.get(id=1)
        expected_max_number = table.max_number
        self.assertEquals(expected_max_number, 2)
        

class ReservationModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='test_user')
        table = Table.objects.create(max_number=2)
        Reservation.objects.create(user=user, table=table, time=timezone.now() + timedelta(days=2), status=False)
        Reservation.objects.create(user=user, table=table, time=timezone.now() - timedelta(days=2), status=False)
        
    def test_str_method(self):
        reservation = Reservation.objects.get(id=1)
        expected_object_name = f'Reservation {reservation.id}'
        self.assertEquals(expected_object_name, f'Reservation {reservation.id}')
        
    def test_if_cancelable(self):
        reservation_future = Reservation.objects.get(id=1)
        reservation_past = Reservation.objects.get(id=2)
        
        self.assertTrue(reservation_future.is_cancelable())
        self.assertFalse(reservation_past.is_cancelable())
        
    def test_process_reservation(self):
        Reservation.process_reservations()
        
        reservation_future = Reservation.objects.get(id=1)
        reservation_past = Reservation.objects.get(id=2)
        
        self.assertFalse(reservation_future.status)
        self.assertTrue(reservation_past.status)