from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)
    failed_login_attempts = models.IntegerField(default=0)
    locked_out_until = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey('auth.Permission', on_delete=models.CASCADE)
