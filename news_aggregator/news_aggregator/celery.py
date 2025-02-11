import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'news_aggregator.settings') # sets the default Django settings module for the Celery program. It ensures that the Django settings are available to Celery.

celery_app = Celery('news_aggregator')

celery_app.conf.beat_schedule = {
    'fetch_news_once_a_day': {
        'task': 'newsApp.tasks.fetch_all',
        'schedule': crontab(hour=3, minute=0),  
    },
    'getrandom_news_once_a_day': {
        'task': 'newsApp.tasks.getrabdom_news_once',
        'schedule': crontab(hour=3, minute=1),  
    },
}


celery_app.config_from_object('django.conf:settings', namespace='CELERY') # configures Celery to use the Django settings module for its configuration
celery_app.autodiscover_tasks() # tells Celery to automatically discover tasks from all installed Django apps
