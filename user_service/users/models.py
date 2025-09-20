# models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum, Case, When, IntegerField
class CustomUser(AbstractUser):
    class LevelStatus(models.TextChoices):
        AGENT = 'AGA', 'Agent'
        SUPERVISOR = 'SPP', 'Senior Supervisor'
        MANAGER = 'SM', 'Senior Manager'
        DIRECTOR = 'SD', 'Senior Director'
    
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


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def current_balance(self):   
        result = self.wallet_transactions.aggregate(
            total_balance=Sum(
                Case(
                    When(type_transaction='CREDIT', then='amount'),
                    When(type_transaction='DEBIT', then=-models.F('amount')),
                    default=0,
                    output_field=IntegerField()
                )
            )
        )
        return result['total_balance'] or 0

    def __str__(self):
        return self.username or f"User ID: {self.id}"