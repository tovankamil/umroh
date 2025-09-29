Sistem Digital Manajemen Jama’ah & Mitra Umroh Project Documentation

Overview
This project is a Django-based user service application with Celery for asynchronous task processing, Redis for caching and message brokering, and multiple modules including banking, sponsorships, and wallet functionality.

Project Structure
text
user_service/
├── api/ # API endpoints
├── bank/ # Banking application
├── sponsorships/ # Sponsorships application
├── users/ # Users application
├── userservice/ # Main project configuration
├── utils/ # Utility functions
├── wallet/ # Wallet application
├── venv/ # Virtual environment
├── **init**.py
├── celery.log # Celery log file
├── manage.py # Django management script
└── requirements.txt # Project dependencies

Prerequisites
Python 3.8+
PostgreSQL
Redis
RabbitMQ (optional, alternative message broker)

Installation & Setup

1. Create Virtual Environment
   python -m venv venv
2. Activate Virtual Environment
   Windows:
   venv\Scripts\activate.bat
   Linux/Mac:
   source venv/bin/activate
3. Install Dependencies
   pip install -r requirements.txt

4. Create Django Apps
   python manage.py startapp bank python manage.py startapp sponsorships python manage.py startapp wallet
5. Database Setup
   python manage.py makemigrations python manage.py migrate

6. Create Superuser
   python manage.py createsuperuser

Running the Application
Start Django Development Server
python manage.py runserver

Start Celery Worker
celery -A userservice worker --loglevel=info

For Debugging Celery
celery -A userservice worker --loglevel=debug --logfile=celery.log --concurrency=2

Check Celery Worker Status
python -m celery -A userservice inspect ping

Redis Operations
redis-cli
Check Celery Task Result
GET celery-task-meta-<task_id>
View All Keys
KEYS \*
Check Memory Usage
INFO memory

Testing
Run Unit Tests
python manage.py test sponsorships.tests

Configuration
Database Configuration
Update userservice/settings.py with your PostgreSQL credentials:
DATABASES = {
'default': {
'ENGINE': 'django.db.backends.postgresql',
'NAME': 'your_db_name',
'USER': 'your_db_user',
'PASSWORD': 'your_db_password',
'HOST': 'localhost',
'PORT': '5432',
}
}

Celery Configuration
Add to userservice/settings.py:

CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672//'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Jakarta'
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 300

Redis Configuration
Add to userservice/settings.py:

CACHES = {
"default": {
"BACKEND": "django_redis.cache.RedisCache",
"LOCATION": "redis://localhost:6379/1",
"OPTIONS": {
"CLIENT_CLASS": "django_redis.client.DefaultClient",
'SOCKET_CONNECT_TIMEOUT': 5, # Add timeout
}
}
}

Application Modules 1. Users Module
User authentication and management
Profile management
Authentication endpoints

    2. Bank Module
        Banking operations
        Transaction processing
        Account management

    3. Sponsorships Module
        Sponsorship management
        Partnership programs
        Campaign tracking

    4. Wallet Module
        Digital wallet functionality
        Payment processing
        Balance management

    5. API Module
        REST API endpoints

API versioning
Documentation
Key Dependencies
x
Django REST Framework: API development
Celery: Asynchronous task queue
Redis: Message broker and caching
PostgreSQL: Database
Psycopg2: PostgreSQL adapter
Django Redis: Redis cache backend
Django Celery Results: Celery result backend

Troubleshooting
Common Issues
Celery connection issues:
-Ensure Redis is running: redis-server
-Check broker URL configuration

Database connection issues:
-Verify PostgreSQL is running
-Check database credentials in settings

Module import errors:
-Ensure virtual environment is activated
-Verify all dependencies are installed

Windows-specific Celery Setup
On Windows, use the solo pool:

python -m celery -A userservice worker --loglevel=info --logfile=celery.log --pool=solo

Development Workflow
1.Activate virtual environment
2.Install new dependencies: pip install <package>
3.Update requirements: pip freeze > requirements.txt
4.Run migrations after model changes
5.Test endpoints using Django development server
6.Monitor Celery tasks using flower or logs

Monitoring
Celery Flower (Monitoring Tool)
pip install flower
celery -A userservice flower
Access at: http://localhost:5555

Log Files
Django logs: Check console output or configure logging in settings

Celery logs: celery.log file in project root

Production Deployment Notes
-Set DEBUG = False in production
-Use environment variables for sensitive data
-Configure proper database connection pooling
-Set up Redis persistence if needed
-Implement proper logging and monitoring
-Use process manager (systemd, supervisor) for Celery

Configure static files serving (Whitenoise, CDN, or web server)
