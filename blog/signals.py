from django.core.mail import send_mail
from .models import Comment, Post
from django.db import models
from django.dispatch import receiver


@receiver(models.signals.post_save, sender=Comment)
def comment_reviewed(sender, instance, **kwargs):
    if instance.is_reviewed and instance.post.author.email:
        send_mail(
            'New comment on your post',
            f"A new comment has been added to your post '{instance.post.title}' by '{instance.name}'."
            'noreply@example.com',
            [instance.post.author.email],
            fail_silently=False,
        )


@receiver(models.signals.post_save, sender=Comment)
def send_notification_comment_mail(sender, instance, **kwargs):
    send_mail(
        'New Comment',
        f"A new comment has been added to '{instance.post.title}' by '{instance.name}':\n\n{instance.message}",
        'noreply@admin.com',
        ['admin@admin.com'],
        fail_silently=False,
    )


@receiver(models.signals.post_save, sender=Post)
def send_notification_post_mail(sender, instance, **kwargs):
    send_mail(
        'New Post',
        f"A new post has been added '{instance.title}' by '{instance.author}'",
        'noreply@admin.com',
        ['admin@admin.com'],
        fail_silently=False,
    )
