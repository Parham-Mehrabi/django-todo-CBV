from django.views.generic import (
    ListView,
    CreateView,
    DeleteView,
    DetailView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Task
from .forms import CreateTaskForm, TaskEditForm, DoneToggleForm
from django.urls import reverse_lazy
from django.shortcuts import redirect


class TodoListView(LoginRequiredMixin, ListView):
    """
    list the authenticated user's tasks and send create from among them
    """

    model = Task
    context_object_name = "tasks"
    template_name = "todo/task_main.html"
    paginate_by = 5

    def get_queryset(self):
        objects = Task.objects.filter(author=self.request.user)
        objects = objects.order_by("-created")
        return objects

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CreateTaskForm()
        return context


class AddTaskView(LoginRequiredMixin, CreateView):
    """
    create new tasks and return to listview page and redirect get requests
    """

    model = Task
    form_class = CreateTaskForm
    success_url = reverse_lazy("todo:todo-list")

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get(self, *args, **kwargs):
        return redirect("todo:todo-list")


class DeleteTask(UserPassesTestMixin, DeleteView):
    """
    handle deleting task, check if the user is either the owner of the task or a superuser
    """

    model = Task
    success_url = reverse_lazy("todo:todo-list")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_superuser

    # TODO SECURITY: change error from 403 to 404 to avoid revealing number of objects in the database


class TaskDetailsView(UserPassesTestMixin, DetailView):
    """
    returns task's details
    """

    model = Task

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_superuser

    # TODO SECURITY: change error from 403 to 404 to avoid revealing number of objects in the database


class UpdateTask(UserPassesTestMixin, UpdateView):
    """
    update the task's details and redirect to task's details
    """

    model = Task
    form_class = TaskEditForm
    template_name = "todo/task_edit.html"
    # success_url = reverse_lazy('todo:todo-list')

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_superuser

    def get_success_url(self):
        return reverse_lazy("todo:details", kwargs={"pk": self.object.id})


class ToggleDone(UserPassesTestMixin, UpdateView):
    """
    toggle status
    """

    model = Task
    form_class = DoneToggleForm
    template_name = "todo/task_edit.html"
    success_url = reverse_lazy("todo:todo-list")

    def test_func(self):
        task = self.get_object()
        return self.request.user == task.author or self.request.user.is_superuser
