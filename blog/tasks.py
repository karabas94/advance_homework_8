from django.core.mail import send_mail as contact_send_mail
from celery import shared_task
from django.contrib.auth import get_user_model

User = get_user_model()


@shared_task
def send_mail(email, subject, text):
    contact_send_mail(email, subject, text, ['admin@admin.com'])
