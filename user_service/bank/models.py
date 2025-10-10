from django.db import models
from django.db import connection

class Bank(models.Model):
    name = models.CharField(max_length=100)
    bank_code = models.CharField(max_length=50, unique=True)
    fee = models.IntegerField(default=0)
    queue = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Auto-fix sequence sebelum menyimpan data baru
        if not self.id:
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT setval('bank_bank_id_seq', (SELECT COALESCE(MAX(id), 0) + 1 FROM bank_bank))")
            except Exception as e:
                print(f"Sequence fix warning: {e}")
        super().save(*args, **kwargs)

    class Meta:
        # Jika nama table berbeda, sesuaikan
        db_table = 'bank_bank'  # Ganti dengan nama table sebenarnya