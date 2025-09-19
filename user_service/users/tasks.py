from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone

from sponsorships.models import Sponsorship
import logging
from celery.exceptions import MaxRetriesExceededError

from django.db import models
from django.db import connection
logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task()
def create_user_task(user_data):

    try:
        
        # Validasi data yang diperlukan
        required_fields = ['username', 'name', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'ktp', 'address', 'province', 'city', 'district',
            'postal_code', 'sponsor_username']
        for field in required_fields:
            if field not in user_data:
                error_msg = f"Field '{field}' tidak ditemukan dalam data user"
                logger.error(error_msg)
                return {'status': 'error', 'message': error_msg}
        
        # Cek apakah user sudah ada
        if User.objects.filter(username=user_data['username']).exists():
            error_msg = f"Username {user_data['username']} sudah terdaftar"
            logger.warning(error_msg)
            return {'status': 'error', 'message': error_msg}
        

        # Gunakan atomic transaction untuk memastikan konsistensi data
        with transaction.atomic():
            # Create user instance
            user = User(
                username=user_data['username'],
                name=user_data['name'],
                phone_number=user_data['phone_number'],
                address= user_data['address'],
                province= user_data['province'],
                city=user_data['city'],  # TAMBAHKAN BARIS INI
                email=user_data['email'],
                first_name=user_data['first_name'],
                last_name=user_data['last_name'],
                district=user_data['district'],
                ktp=user_data['ktp'],
                postal_code=user_data['postal_code'],
                date_joined=timezone.now()
            )
            
            # Set password properly (this hashes the password)
            user.set_password(user_data['password'])
            
            # Save the user
            user.save()
            
            # Create Sponsorship data
            sponsor_username = user_data.get('sponsor_username')
            if sponsor_username:
                try:
                    # Dapatkan sponsor berdasarkan username
                    sponsor = User.objects.get(username=sponsor_username)
                    Sponsorship.objects.create(
                        user=user,
                        sponsor=sponsor
                    )
                except User.DoesNotExist:
                    logger.warning(f"Sponsor dengan username {sponsor_username} tidak ditemukan")
                    # Tidak perlu rollback, sponsorship opsional
                except Exception as e:
                    logger.error(f"Error creating sponsorship: {str(e)}")
                    # Tidak perlu rollback, sponsorship opsional
        
        logger.info(f"User {user.username} berhasil dibuat melalui Celery (ID: {user.id})")
        SponsorshipQuerySet(m
        return {
            'status': 'success', 
            'username': user.username,
            'email': user.email,
            'alamat': user.address,
            'ktp':user.ktp
        }
        
    except IntegrityError as e:
        logger.error(f"IntegrityError saat membuat user: {str(e)}")
        return {'status': 'error', 'message': 'Data user tidak valid atau duplikat'}
        
    except Exception as e:
        logger.error(f"Error tidak terduga saat membuat user: {str(e)}")
        
        # Coba ulang task untuk exception tertentu
        try:
            if "database" in str(e).lower() or "connection" in str(e).lower():
                create_user_task.retry(exc=e, countdown=60)
        except MaxRetriesExceededError:
            logger.critical(f"Gagal membuat user setelah 3 percobaan")
        
        return {'status': 'error', 'message': 'Terjadi kesalahan sistem saat membuat user'}

class SponsorshipQuerySet(models.QuerySet):
    def with_upline(self, user_id):
        query = """WITH RECURSIVE user_upline AS (
    -- Bagian Jangkar: Mulai dari baris pengguna yang kamu pilih.
    SELECT
        id,
        user_id,
        sponsor_id,
        0 AS level
    FROM
        sponsorships_sponsorship
    WHERE
        user_id = '81b028bd-01a3-45a0-b7fe-0ee862199024' -- Ganti dengan user_id yang kamu cari
    
    UNION ALL
    
    -- Bagian Rekursif: Cari sponsor sebelumnya dengan mencocokkan sponsor_id dengan user_id.
    SELECT
        t.id,
        t.user_id,
        t.sponsor_id,
        h.level + 1
    FROM
        sponsorships_sponsorship t
    JOIN
        user_upline h ON h.sponsor_id = t.user_id
    WHERE
        h.sponsor_id IS NOT NULL
		  AND h.level < 2
)
-- Akhirnya, pilih semua hasil dari CTE rekursif.
SELECT * FROM user_upline;""" # Gunakan kueri yang sama seperti di atas
        return self.raw(query, [user_id])
