from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    FARMER = 'farmer'
    CONSUMER = 'consumer'

    ROLE_CHOICES = [
        (FARMER, 'Farmer'),
        (CONSUMER, 'Consumer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
