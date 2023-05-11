from celery import shared_task
from django.contrib.auth import get_user_model
import random
from faker import Faker
from todo.models import Task

User = get_user_model()


@shared_task
def clean_done_tasks():
    Task.objects.filter(is_complete=True).delete()
    return 'all completed tasks deleted'


@shared_task
def create_random_task():
    """ create random task for a user """
    fake = Faker()
    users = User.objects.all()
    task = Task.objects.create(
        author=random.choice(users),
        title=fake.paragraph(nb_sentences=1),
        context=fake.paragraph(nb_sentences=5),
        is_complete=random.choice([True, False])
    )
    task.save()
    return f'Task created title: {task.title}'
