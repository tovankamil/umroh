
import uuid
from django.db import models
from bank.models import Bank
from django.conf import settings

class Nasabah(models.Model):  
    id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='nasabah_profiles'
    )
    bank = models.ForeignKey(
        Bank,
        on_delete=models.CASCADE,
        related_name='nasabah_list'
    )
    nasabah_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=20, unique=True)
    branch = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.name} - {self.account_number} ({self.bank.name}) {self.branch} "