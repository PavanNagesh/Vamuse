# views.py
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .models import User
from django.db import connection
from django.contrib.auth.hashers import check_password
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth import authenticate, login
import time
from django.conf import settings
from datetime import datetime, timedelta
from django.core.mail import send_mail
import random



def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return redirect('signin')
        
        # Check if the email or username already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email is already used.')
            return redirect('signin')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken.')
            return redirect('signin')
        
        try:
            # Create a new user instance and save it to the database
            user = User.objects.create(username=username, email=email, password=password)
            messages.success(request, 'You are now registered and can log in.')
            return redirect('login')  # Redirect to the login page after successful sign-up
        except IntegrityError:
            messages.error(request, 'An error occurred while saving your data. Please try again.')
            return redirect('signin')
            
    return render(request, 'signin.html')



def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user using username and password
        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            user.last_login = timezone.now()
            user.save()

            # Generate OTP
            otp = ''.join(random.choices('0123456789', k=6))  # Generate a 6-digit OTP
            request.session['otp'] = otp  # Store OTP in session

            # Send OTP to user's email
            send_mail(
                'Your OTP for Login Verification',
                f'Your OTP is: {otp}',
                'sender@example.com',  # Replace with your sender email
                [user.email],  # Send OTP to user's email
                fail_silently=False,
            )

            # Redirect user to OTP verification page
            return redirect('otp_verification')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
    else:
        return render(request, 'login.html')

# Define the OTP verification view
def otp_verification(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')

        # Retrieve OTP from session
        otp = request.session.get('otp')

        # Validate entered OTP
        if entered_otp == otp:
            # OTP is valid, redirect user to home page or desired destination
            return redirect('index')
        else:
            return render(request, 'otp_verification.html', {'error': 'Invalid OTP. Please try again.'})
    else:
        return render(request, 'otp_verification.html')
    
def user_profile(request):
    # Assuming user is already authenticated
    # You can access user's details via request.user
    return render(request, 'userprofile.html', {'user': request.user})

def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to your login page URL


def index(request):
    return render(request, 'index.html')

def innerpage(request):
    return render(request, 'innerpage.html')

def portfolio(request):
    return render(request, 'portfolio.html')

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def header(request):
    return render(request, 'header.html')

def footer(request):
    return render(request, 'footer.html')

def services(request):
    return render(request, 'services.html')

def home(request):
    return render(request, 'home.html')


@login_required
def change(request):
    if request.method == 'POST':
        new_email = request.POST.get('new_email')
        # Update user's email in the database
        request.user.email = new_email
        request.user.save()
        return redirect('userprofile')  # Redirect to the user profile page after updating the email
    return render(request, 'change.html')  # Render the change email page

def safety(request):
    return render(request, 'safety.html')

def rules(request):
    return render(request, 'rules.html')

@login_required
def update(request):
    # Handle form submission via POST request
    if request.method == 'POST':
        new_username = request.POST.get('username')
        new_email = request.POST.get('email')
        # Retrieve the current user
        user = request.user
        # Update the user's username
        if new_username:
            user.username = new_username
        # Update the user's email
        if new_email:
            user.email = new_email
        # Save the updated user data
        user.save()
        # Provide feedback to the user
        messages.success(request, "Profile updated successfully!")
        # Redirect the user to their profile page
        return redirect('userprofile')
    # Render the update profile form for GET requests
    return render(request, 'update.html')

