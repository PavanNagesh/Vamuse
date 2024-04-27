from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)  # Adding username field
    password = models.CharField(max_length=128)
    failed_login_attempts = models.IntegerField(default=0)
    last_failed_login_attempt = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.username

    def increase_failed_login_attempts(self):
        self.failed_login_attempts += 1
        self.last_failed_login_attempt = timezone.now()
        self.save()

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.last_failed_login_attempt = None
        self.save()

    def is_locked_out(self):
        # Define your lockout logic here (e.g., lockout after 5 failed attempts)
        # This method should return True if the user is currently locked out, False otherwise
        pass

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
