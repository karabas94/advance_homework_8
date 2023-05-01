from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from faker import Faker

fake = Faker()


class Command(BaseCommand):
    help = 'Create users'  # noqa: A003

    def handle(self, *args, **options):
        # create 10 users
        user = []
        for _ in range(10):
            user.append(User(username=fake.first_name(), email=fake.email(),
                             password=make_password(fake.password())))
        User.objects.bulk_create(user)

        self.stdout.write(self.style.SUCCESS(f'Successfully created {len(user)} user(s)'))
