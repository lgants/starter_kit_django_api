from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=128, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_profile = models.ForeignKey('users.UserProfile', blank=True, null=True, on_delete=models.CASCADE)


class UserProfile(models.Model):
    first_name = models.CharField(max_length=128, unique=True)
    last_name = models.CharField(max_length=128, unique=True)
