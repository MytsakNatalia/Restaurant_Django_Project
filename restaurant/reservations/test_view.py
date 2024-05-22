from django.test import TestCase, Client
from django.urls import reverse
from reservations.models import *
from users.models import User

class TestViewsReservations(TestCase):
    def setUp(self):        
        self.client = Client()       

        # Create a User              
        self.user = User.objects.create_user(username='test_user', password='password')
        
        # Authenticate the user
        self.client.login(username='test_user', password='password')

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

    
    def test_book_table_view_get(self):        
        response = self.client.get(reverse('reservations:booktbl'))
        self.assertEqual(response.status_code, 200)        
        self.assertTemplateUsed(response, 'reservations/booktbl.html')

    def test_book_table_view_post_success(self):
        # Test POST request for booking a table successfully
        date_str = (timezone.now() + timedelta(days=2)).strftime('%Y-%m-%d')
        time_str = (timezone.now() + timedelta(days=2)).strftime('%H:%M')    
        data = {
            'people': 2,
            'date': date_str,
            'time': time_str
        }
        response = self.client.post(reverse('reservations:booktbl'), data)
        self.assertEqual(response.status_code, 302)  

        # Check if the reservation was created
        new_reservation = Reservation.objects.last()
        self.assertEqual(new_reservation.user, self.user)
        self.assertEqual(new_reservation.table, self.table)
        
    def test_book_table_view_post_invalid_data(self):
        # Test POST request for booking a table with invalid data
        data = {}  
        response = self.client.post(reverse('reservations:booktbl'), data)
        self.assertEqual(response.status_code, 302)  
