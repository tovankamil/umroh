from celery import shared_task
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.db import IntegrityError, transaction
from django.utils import timezone
from .models import CustomUser
from sponsorships.models import Sponsorship
import logging
from celery.exceptions import MaxRetriesExceededError

logger = logging.getLogger(__name__)
User = get_user_model()

@shared_task()
def create_user_task(user_data):

    try:
        # Validasi data yang diperlukan
        required_fields = ['username', 'name', 'email', 'password', 'first_name', 'last_name',
            'phone_number', 'ktp', 'address', 'province', 'city', 'district',
            'postal_code', 'sponsor_username']
        # for field in required_fields:
        #     if field not in user_data:
        #         error_msg = f"Field '{field}' tidak ditemukan dalam data user"
        #         logger.error(error_msg)
        #         return {'status': 'error', 'message': error_msg}
        
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
                email=user_data['email'],
                first_name=user_data.get('first_name', ''),
                last_name=user_data.get('last_name', ''),
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
        
        # # Kirim email welcome secara asynchronous
        # send_welcome_email.delay(user.id)
        
        logger.info(f"User {user.username} berhasil dibuat melalui Celery (ID: {user.id})")
        
        return {
            'status': 'success', 
           
            'username': user.username,
            'email': user.email
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


