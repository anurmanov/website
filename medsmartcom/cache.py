from django.core.cache import cache
from django.conf import settings
import os

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

cache.set('key', 'value', 60)
