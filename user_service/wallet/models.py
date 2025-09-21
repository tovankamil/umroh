from django.db import models
from django.core.validators import MinValueValidator
from django.conf import settings
from decimal import Decimal
import uuid  # Import uuid yang hilang

# Wallet Transaction Model harus didefinisikan SEBELUM WalletSummary
# karena WalletSummary memiliki ForeignKey ke wallet_transaction

class WalletTransaction(models.Model):  
    class TransactionType(models.TextChoices):
        DEBIT = 'DEBIT', 'Debit'
        CREDIT = 'CREDIT', 'Credit'
    
    class BonusType(models.TextChoices):
        REFERRAL = 'REFERRAL', 'Referral Bonus'
        COMMISSION = 'COMMISSION', 'Commission'
        CASHBACK = 'CASHBACK', 'Cashback'
        REWARD = 'REWARD', 'Reward'
        OTHER = 'OTHER', 'Other'

    id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet_transactions'
    )
    
    type_transaction = models.CharField(
        max_length=6,
        choices=TransactionType.choices
    )
    
    type_bonus = models.CharField(
        max_length=20,
        choices=BonusType.choices,
        blank=True,
        null=True
    )
    
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))]
    )
    
    # Reference to another user if applicable (e.g., referral)
    reference_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='referred_transactions'
    )
    
    transfer_transaction= models.CharField(max_length=150,default="",null=True,blank=True)
    description = models.TextField(blank=True, null=True)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        indexes = [
            models.Index(fields=['user', 'created_at']),
            models.Index(fields=['transfer_transaction']),
            models.Index(fields=['created_at']),
        ]
        ordering = ['-created_at']
        verbose_name = "Wallet Transaction"
        verbose_name_plural = "Wallet Transactions"
    
    def save(self, *args, **kwargs):
        if not self.transfer_transaction:
            # Generate unique transaction ID
            self.transfer_transaction = f"TX{uuid.uuid4().hex[:16].upper()}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.username} - {self.type_transaction} - {self.amount}"


class WalletSummary(models.Model):
    """Summary table for faster balance queries"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wallet_summary'
    )
    
    current_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )
    
    last_transaction = models.ForeignKey(
        WalletTransaction,  # Menggunakan nama class yang benar
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Wallet Summaries"
    
    def __str__(self):
        return f"{self.user.username} - Balance: {self.current_balance}"