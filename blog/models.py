from django.db import models
from django.conf import settings
from django.shortcuts import reverse


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

    def get_absolute_url(self):
        """Returns the url to access a particular post instance."""
        return reverse('blog:post_detail', args=[str(self.id)])


class Comment(models.Model):
    name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name
