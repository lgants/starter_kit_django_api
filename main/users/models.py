from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=128, unique=True)
    role = models.CharField(max_length=128, default='user')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserProfile(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class AuthCertificate(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    serial = models.CharField(max_length=128, unique=True)


class AuthFacebook(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    fb_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)


class AuthGithub(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    gh_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)


class AuthGoogle(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    google_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)


class AuthLinkedin(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    ln_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)
