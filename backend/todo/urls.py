from django.urls import path
from .views import TodoListView, AddTaskView, DeleteTask, TaskDetailsView, UpdateTask, ToggleDone

app_name = 'todo'

urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('add/', AddTaskView.as_view(), name='add-task'),
    path('delete/<int:pk>', DeleteTask.as_view(), name='delete'),
    path('details/<int:pk>', TaskDetailsView.as_view(), name='details'),
    path('update/<int:pk>', UpdateTask.as_view(), name='edit'),
    path('toggle/<int:pk>', ToggleDone.as_view(), name='toggle'),
]
