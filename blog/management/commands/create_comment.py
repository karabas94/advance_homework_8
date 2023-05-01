from django.core.management.base import BaseCommand
from blog.models import Comment, Post
from faker import Faker
from random import randint, choice
from django.utils import timezone
from datetime import timedelta

fake = Faker()


class Command(BaseCommand):
    help = 'Create comments'  # noqa: A003

    def handle(self, *args, **options):
        # create 1000 comments
        comment = []
        for _ in range(1000):
            comment.append(Comment(
                name=fake.first_name(),
                message=fake.sentence(nb_words=10),
                created_at=timezone.now() - timedelta(days=randint(0, 499)),
                is_reviewed=True,
                post=choice(Post.objects.all())
            ))
        Comment.objects.bulk_create(comment)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(comment)} comment(s)'))
