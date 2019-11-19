import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'medsmartcom.settings')

app = Celery('medsmartcom')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks()
app.conf.result_expires = 60