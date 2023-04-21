from rest_framework.viewsets import ModelViewSet
from ..models import Task
from .serializers import TaskSerializer


class TaskViewSet(ModelViewSet):
    model = Task
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(author=user)
