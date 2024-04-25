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
from django.http import HttpResponseForbidden



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



from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import render, redirect
from django.db import connection
from django.utils import timezone
from django.http import Http404

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        query = f"SELECT * FROM amuse_user WHERE username = '{username}' AND password = '{password}'"

        with connection.cursor() as cursor:
            cursor.execute(query)
            row = cursor.fetchone()

        if row:
            user = authenticate(username=username, password=password)
            if user is not None:
                user.last_login = timezone.now()
                user.save()
                auth_login(request, user)
                return redirect('index')
            else:
                raise Http404("User authentication failed.")
        else:
            # Log failed login attempts
            request.session.setdefault('login_attempts', 0)
            request.session['login_attempts'] += 1
            
            # Check if login attempts exceed limit
            if request.session['login_attempts'] >= 5:
                last_attempt_time = request.session.get('last_attempt_time')
                if last_attempt_time and timezone.now() < last_attempt_time + timezone.timedelta(seconds=300):
                    # Calculate remaining time
                    remaining_time = (last_attempt_time + timezone.timedelta(seconds=300) - timezone.now()).seconds
                    raise Http404(f"Too many login attempts. Please try again in {remaining_time} seconds.")
                
                # Reset login attempts counter and update last attempt time
                request.session['login_attempts'] = 1
                request.session['last_attempt_time'] = timezone.now()
                    
            return render(request, 'login.html', {'error': 'Invalid username or password.'})
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

