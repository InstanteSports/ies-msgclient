import requests

from celery import shared_task
from celery.task.schedules import crontab
from celery.decorators import periodic_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)

@shared_task
def boot_up():
    print("Task Activated, so task sending should work now")

@periodic_task(run_every=(crontab(minute='*/5')), name="celery_ping", ignore_result=True)
def celery_ping():
    from .manager import send_ping
    send_ping('celery-alive', 10)
