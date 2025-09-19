# my_crud_api/celery.py

import os
from celery import Celery
from celery.schedules import crontab
# Setel default Django settings module.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'userservice.settings')

app = Celery('userservice')

# Menggunakan string di sini untuk Celery tidak perlu
# "pickle" the object ketika worker memproses.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Muat task modules dari semua aplikasi Django terdaftar.

app.conf.update(
    task_acks_late=True,
    task_reject_on_worker_lost=True,
    task_track_started=True,
    worker_prefetch_multiplier=1,  # Kurangi prefetching untuk prioritaskan task yang tidak throttled
    task_compression = 'gzip',
    result_compression = 'gzip',
    worker_disable_rate_limits=True,
    worker_max_tasks_per_child=200,
)

# Auto-discover tasks
app.autodiscover_tasks()

# Scheduled tasks untuk membersihkan cache throttling
app.conf.beat_schedule = {
    'cleanup-throttle-cache': {
        'task': 'your_app.tasks.cleanup_throttle_cache',
        'schedule': crontab(hour=3, minute=0),  # Setiap hari jam 3 pagi
    },
}