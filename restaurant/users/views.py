
# Create your views here.
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from  users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse
from shopping_cart.models import ShoppingCart
# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if(not ShoppingCart.objects.filter(user=user, is_active=True).exists()):
                    ShoppingCart.objects.create(user=user, is_active=True)
                return   HttpResponseRedirect(reverse('index'))
    else:
        form = UserLoginForm()
    context = {'form':form}
    return  render(request, 'users/login.html', context)

def registartion(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Congratulations! You`ve created an account')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)
            context = {'form': form}
            return  render(request, 'users/register.html', context)

    else:
        form = UserRegistrationForm()
    context = { 'form' : form }
    return  render(request, 'users/register.html', context)

def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data = request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return  HttpResponseRedirect(reverse('index'))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    context = {'form': form, 'baskets': ShoppingCart.objects.filter(user=request.user)}
    return  render(request, 'users/profile.html', context)

def logout(request):
    auth.logout(request)
    return  HttpResponseRedirect(reverse('index'))