from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
import logging

logger = logging.getLogger(__name__)
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_backend.settings')

app = Celery('django_backend')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related config keys should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
app.conf.broker_connection_retry_on_startup = True
# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


app.conf.beat_schedule = {
    'send-daily-property-report': {
        'task': 'property.tasks.send_property_report',
        'schedule': crontab(minute=1, hour=0),  # Every day at 00:01
    },
}

@app.task(bind=True)
def debug_task(self):
    logger.debug('Request: {0!r}'.format(self.request))