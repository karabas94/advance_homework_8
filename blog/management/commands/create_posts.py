from django.core.management.base import BaseCommand
from faker import Faker
from blog.models import Post
from random import randint, choice
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

fake = Faker()


class Command(BaseCommand):
    help = 'Create posts'  # noqa: A003

    def handle(self, *args, **options):
        # create 2000 posts
        post = []
        for _ in range(2000):
            post.append(Post(
                title=fake.sentence(nb_words=5),
                short_description=fake.paragraph(nb_sentences=3),
                text=fake.paragraph(nb_sentences=7),
                image='images/grey_336x280.gif',
                author=choice(User.objects.all()),
                created_at=timezone.now() - timedelta(days=randint(500, 1000)),
                is_draft=False
            ))
        Post.objects.bulk_create(post)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(post)} post(s)'))
