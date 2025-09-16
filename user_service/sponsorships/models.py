# models.py Sponsorship

from django.db import models
from django.conf import settings

class Sponsorship(models.Model):
    # Mengacu pada user yang disponsori
    # related_name='sponsored_by_me' akan memungkinkan Anda mengakses semua
    # sponsorship yang dibuat oleh user ini.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sponsored_by_me'
    )
    
    # Mengacu pada sponsor user. 
    # self-referential many-to-one relationship.
    # related_name='my_sponsorships' akan memungkinkan Anda mengakses
    # relasi sponsorship dari sisi user.
    sponsor = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='my_sponsorships',
        blank=True,
        null=True
    )
    
    user_level = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        # Memastikan tidak ada error jika user belum ada
       try:
            user_name = self.user.username if self.user else "N/A"
            sponsor_name = self.sponsor.username if self.sponsor else "N/A"
            return f"User: {user_name} sponsor:{sponsor_name}"
       except (AttributeError, settings.AUTH_USER_MODEL.DoesNotExist):
            return f"Sponsorship ID: {self.pk}"