from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

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

    def get_absolute_api_url(self):
        return reverse('todo:api-v1:tasks-detail', kwargs={'pk': self.pk})
