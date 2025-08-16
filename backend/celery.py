import os
from celery import Celery

# 1. Tell Celery how to find your Django project's settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

# 2. Create the Celery application instance
app = Celery('backend')

# 3. Load the configuration from your Django settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# 4. Tell Celery to automatically find tasks in all your Django apps
app.autodiscover_tasks()