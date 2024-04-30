from django.urls import path, include
from users.views import login, registartion, profile, logout
app_name = 'users'
urlpatterns = [
    path('login/', login, name='login' ),
    path('register/', registartion, name='registration'),
    path('profile/', profile, name='profile'),
    path('logout/', logout, name='logout')
]