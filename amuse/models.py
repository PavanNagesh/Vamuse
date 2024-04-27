from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)

    def __str__(self):
        return self.username

class LoginAttempt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login_attempt = models.DateTimeField(null=True, blank=True)
