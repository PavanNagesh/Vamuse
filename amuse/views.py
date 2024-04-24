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



from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
import time

failed_login_attempts = {}

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Check if the user has exceeded the maximum number of failed attempts within a time period
        if username in failed_login_attempts:
            attempts, last_attempt_time = failed_login_attempts[username]
            if time.time() - last_attempt_time < 60:  # Time period in seconds (e.g., 60 seconds)
                # Too many failed attempts within the time period, show error and prevent login
                messages.error(request, 'Too many failed login attempts. Please try again later.')
                return render(request, 'login.html')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Login successful, reset failed login attempts and redirect to home page
            del failed_login_attempts[username]  # Reset failed attempts if login is successful
            login(request, user)
            return redirect('index')
        else:
            # Login failed, track the attempt and display error message
            failed_login_attempts[username] = (failed_login_attempts.get(username, (0, 0))[0] + 1, time.time())
            messages.error(request, 'Invalid username or password.')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

    
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

