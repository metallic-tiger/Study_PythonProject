from celery import Celery
from django.conf import settings
from django.core.mail import send_mail
from time import sleep
import os
import django 

django.setup()
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dailyfresh.settings")
app = Celery('celery_task.tasks',backend = 'redis://192.168.142.142:6379/1')

@app.task
def Send_active_Email(subject , msg , sender , re , html):
    send_mail(subject,msg,sender,rec,html_message=html)