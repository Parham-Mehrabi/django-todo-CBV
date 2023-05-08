import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from faker import Faker
from todo.models import Task

User = get_user_model()


class Command(BaseCommand):
    """
        a costume command that creates 5 tasks each time it runs
    """

    help = "create 5 tasks in each run"

    def __init__(self, *args, **kwargs):
        self.fake = Faker()
        super().__init__(*args, **kwargs)

    def handle(self, *args, **options):
        email = self.fake.email()
        while True:
            try:
                user = User.objects.create_user(email=email, password='faker654321')
                for _ in range(5):
                    Task.objects.create(
                        author=user,
                        title=self.fake.paragraph(nb_sentences=1),
                        context=self.fake.paragraph(nb_sentences=5),
                        is_complete=random.choice([True, False])
                    )
                break
            except IntegrityError:
                print(f'user with email {email} already exists')
                email = self.fake.email()
                print(f'trying new email: {email}')
