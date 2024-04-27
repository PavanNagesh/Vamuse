from django.contrib.auth.models import AbstractUser, Group, Permission
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

    def increment_failed_login_attempts(self):
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 5:
            self.locked_out_until = timezone.now() + timezone.timedelta(minutes=1)
            self.failed_login_attempts = 0
        self.save()

    def reset_failed_login_attempts(self):
        self.failed_login_attempts = 0
        self.locked_out_until = None
        self.save()

class UserGroup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

class UserPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
