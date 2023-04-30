from django.apps import AppConfig

from django.db.models.signals import post_save


class BlogConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'

    def ready(self):
        from .signals import send_notification_comment_mail, send_notification_post_mail, comment_reviewed
        from .models import Comment, Post
        post_save.connect(send_notification_comment_mail, sender=Comment)
        post_save.connect(send_notification_post_mail, sender=Post)
        post_save.connect(comment_reviewed, sender=Comment)
