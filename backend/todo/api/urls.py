from django.urls import path
from .views import TaskViewSet
from rest_framework.routers import DefaultRouter

app_name = "api-1"

router = DefaultRouter()

router.register(basename="tasks", viewset=TaskViewSet, prefix="task")

urlpatterns = [
    # path('task/', TaskViewSet.as_view(),),
]
urlpatterns += router.urls
