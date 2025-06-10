from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from .models import Product, Category, About, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm, UpdateUserForm, ChangePasswordForm, UserInfoForm
from payment.forms import ShippingForm
from payment.models import ShippingAddress
from django import forms
import json
from cart.cart import Cart




def update_info(request):
    if request.user.is_authenticated:
        try:
            current_user = Profile.objects.get(user__id=request.user.id)
        except Profile.DoesNotExist:
            messages.error(request, "Profile not found.")
            return redirect('home')

        try:
            shipping_user = ShippingAddress.objects.get(user__id=request.user.id)
        except ShippingAddress.DoesNotExist:
            shipping_user = ShippingAddress(user=request.user)  # create unsaved instance

        form = UserInfoForm(request.POST or None, instance=current_user)
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        if form.is_valid() and shipping_form.is_valid():
            form.save()
            shipping_form.save()
            messages.success(request, 'Info eshte perditsuar')
            return redirect('home')

        return render(request, 'update_info.html', {'form': form, 'shipping_form': shipping_form})
    else:
        messages.error(request, 'Ti duhesh te logohesh ne menyre qe te kesh akses ne kete faqe')
        return redirect('home')


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        # Did they fill out the form
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            # Is the form valid
            if form.is_valid():
                form.save()
                messages.success(request, "Passwordi juaj eshte perditsuar")
                login(request, current_user)
                return redirect('update_user')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update_password')
        else:
            form = ChangePasswordForm(current_user)
            return render(request, "update_password.html", {'form': form})
    else:
        messages.success(request, "Si fillim duhesh te logohesh!")
        return redirect('home')


def update_user(request):
    if request.user.is_authenticated:
        current_user = User.objects.get(id=request.user.id)
        user_form = UpdateUserForm(request.POST or None, instance=current_user)

        if user_form.is_valid():
            user_form.save()

            login(request, current_user)
            messages.success(request, 'Useri eshte perditsuar')
            return redirect('home')
        return render(request, 'update_user.html', {'user_form': user_form})
    else:
        messages.success(request, 'Ti duhesh te logohesh ne menyre qe te kesh akses ne kete faqe')
        return redirect('home')


def category(request, foo):
    try:
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category_name': category.name})
    except:
        messages.error(request, 'Category does not exist')
        return redirect('home')


def product(request, pk):
    product = Product.objects.get(id=pk)
    return render(request, 'product.html', {'product': product})


def home(request):
    products = Product.objects.all()
    return render(request, 'home.html', {'products': products})


def about(request):
    about = About.objects.all().first()
    return render(request, 'about.html', {'about': about})


def login_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                #Do some shopping cart stuff
                current_user = Profile.objects.get(user__id=request.user.id)
                #Get their saved cart from database
                saved_cart= current_user.old_cart
                # Convert database string to python dictionary
                if saved_cart:
                    #Covert to dictionary using JSON
                    converted_cart=json.loads(saved_cart)
                    # Add the loaded cart dicitionary to our session
                    # Get cart
                    cart= Cart(request)
                    #Loop through the cart and add the items from the database
                    for key,value in converted_cart.items():
                        cart.db_add(product=key, quantity=value)


                messages.success(request, 'Tani ke hyre ne account!')
                return redirect('home')
        else:
            messages.error(request, 'Eshte nje problem ti nuk ke hyre ne account!')
            return redirect('login')
    else:
        return render(request, 'login.html')


def logout_user(request):
    logout(request)
    messages.success(request, 'Ti dole nga accounti!')
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
                messages.success(request, 'Username u kriu. Te lutem krijo user info!')
                return redirect('update_info')
            else:
                messages.error(request, 'Eshte nje problem me autentikimin!')
                return redirect('register')
        else:
            messages.error(request, 'Oops! Eshte nje problem me regjistrimin!')
    else:
        form = SignUpForm()

    return render(request, 'register.html', {'form': form})
