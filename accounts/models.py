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