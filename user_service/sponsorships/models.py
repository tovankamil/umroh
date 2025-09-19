# models.py - Perbaikan model
from django.db import models
from django.conf import settings

class Sponsorship(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sponsored_by_me'
    )
    
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='my_sponsorships',
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['sponsor']),
            models.Index(fields=['user']),
        ]

    def __str__(self):
        return f"{self.user.username} sponsored by {self.sponsor.username if self.sponsor else 'None'}"