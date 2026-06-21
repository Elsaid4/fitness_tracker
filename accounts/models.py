# Create your models here.
# accounts/models.py
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('user', 'Standard User'),
        ('coach', 'Coach'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username

    def is_coach(self):
        return self.role == 'coach'

class Profile(models.Model):
    user            = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name            = models.TextField(blank=True, null=True)
    last_name       = models.TextField(blank=True, null=True)
    bio             = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    address         = models.CharField(max_length=255, blank=True, null=True)
    phone_number    = models.CharField(max_length=20, blank=True, null=True)
    weight          = models.FloatField(blank=True, null=True)
    height          = models.FloatField(blank=True, null=True)
    date_of_birth   = models.DateField(blank=True, null=True)


    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    @property
    def age(self):
        if self.date_of_birth:
            today = date.today()
            return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return None