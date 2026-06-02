# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('coach', 'Coach'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    def is_coach(self):
        return self.role == 'coach'

class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

class ProfileManager(models.Manager):
    def coaches(self):
        return self.filter(user__role='coach')