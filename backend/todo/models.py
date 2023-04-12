from django.db import models
from django.contrib.auth import get_user_model

user = get_user_model()
# Create your models here.


class Task(models.Model):
    author = models.ForeignKey(user, on_delete=models.CASCADE, blank=True)

    title = models.CharField(max_length=120, blank=False)
    context = models.TextField(blank=True)
    is_complete = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
