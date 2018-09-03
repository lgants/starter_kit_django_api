from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):
    username = models.CharField(max_length=256, unique=True)
    email = models.CharField(max_length=128, unique=True)
    role = models.CharField(max_length=128, default='user')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()


class UserProfile(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='profile')
    avatar_url = models.CharField(blank=True, null=True, max_length=256)
    bio = models.TextField(blank=True, null=True, max_length=512) # TODO: determine if partner sites possess similiar limit; would fail otherwise
    first_name = models.CharField(blank=True, null=True, max_length=128)
    last_name = models.CharField(blank=True, null=True, max_length=128)

    @property
    def full_name(self):
        return "{} {}".format(self.first_name, self.last_name)


class AuthCertificate(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    serial = models.CharField(max_length=128, unique=True)


class AuthFacebook(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='auth_facebook')
    fb_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)
    response = models.TextField()


class AuthGithub(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='auth_github')
    gh_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)
    response = models.TextField()


class AuthGoogle(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='auth_google')
    google_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)
    response = models.TextField()


class AuthLinkedin(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE, related_name='auth_linkedin')
    ln_id = models.CharField(max_length=256, unique=True)
    display_name = models.CharField(max_length=256)
    response = models.TextField()
