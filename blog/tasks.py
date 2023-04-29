from django.core.mail import send_mail as contact_send_mail
from celery import shared_task


@shared_task
def send_mail(email, subject, text):
    contact_send_mail(email, subject, text, ['admin@admin.com'])
