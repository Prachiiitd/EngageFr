from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import Group

from .forms import CreateUserForm
from .decorators import unauthenticated_user
from .models import Customer
# Create your views here.


@unauthenticated_user
def index(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            # group = None
            try:
                group = Group.objects.get(name='customer')
            except Group.DoesNotExist:
                Group.objects.create(name='customer')
                group = Group.objects.get(name='customer')

            user.groups.add(group)

            customer = Customer(user=user, fName=user.first_name, lName=user.last_name, email=user.email)
            customer.save()

            messages.success(request, f'Account created for {username}!')
        else:
            for field, errors in form.errors.items():
                messages.error(request, f'{field}: {errors}')

        return redirect('Auth:authIndex')

    else:
        return render(request, 'auth/login.html', {'form': form})


@unauthenticated_user
def loginUser(request):
    if request.user.is_authenticated:
        return redirect('Customer:dashboard')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('Customer:dashboard')
            else:
                messages.error(request, f'Login failed! Please try again.')
        return redirect('Auth:authIndex')


def logoutUser(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, f'Logout successful!')
    else:
        messages.error(request, f'Logout failed! Please try again.')
    return redirect('Auth:authIndex')
