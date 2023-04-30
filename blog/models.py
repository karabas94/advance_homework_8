from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail


class Post(models.Model):
    title = models.CharField(max_length=255)
    short_description = models.TextField()
    text = models.TextField()
    image = models.ImageField(upload_to='images/', blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_draft = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name


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
