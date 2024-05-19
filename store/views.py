from django.shortcuts import render, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    return render(request, 'about.html')


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You are now logged in')
                return redirect('home')
        else:
            messages.success(request, 'There is an error! You are not logged in')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Since the form is valid, we can directly access the cleaned data for authentication
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, 'You have been registered successfully')
                return redirect('home')
            else:
                messages.error(request, 'There was an issue with authentication')
                return redirect('register')
        else:
            messages.error(request, 'Oops! There was a problem with your registration')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})