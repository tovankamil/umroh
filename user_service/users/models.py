# models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    class LevelStatus(models.TextChoices):
        AGENT = 'AGA', 'Agent'
        SUPERVISOR = 'SPV', 'Supervisor'
        DIRECTOR = 'DRC', 'Director'
    
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    username = models.CharField(max_length=255, unique=True, null=True, blank=True)  
    name = models.CharField(max_length=255, blank=True, null=True)
    phone_number = models.CharField(max_length=16, blank=True, null=True)
    ktp = models.CharField(max_length=16, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    province = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)  
    district = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=10, blank=True, null=True)
    ahliwaris = models.CharField(max_length=255, blank=True, null=True)
    level_status = models.CharField(
        max_length=3,
        choices=LevelStatus.choices,
        default=LevelStatus.AGENT
    )

    def __str__(self):
        return self.username or f"User ID: {self.id}"