from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from django.contrib.auth import get_user_model
from .forms import RegisterForm
from django.urls import reverse_lazy

user = get_user_model()


class TodoLogoutView(LogoutView, LoginRequiredMixin):
    """
    Log out the user and redirect to login Page.
    """

    next_page = reverse_lazy("account:login")


class TodoRegisterView(CreateView):
    """
    handle new users
    """

    template_name = "registration/register.html"
    model = user
    form_class = RegisterForm
    success_url = reverse_lazy("todo:todo-list")


class TodoLoginView(LoginView):
    """
        login and redirect user to home
    """
    template_name = 'registration/login.html'
    model = user
    success_url = reverse_lazy("todo:todo-list")
    next_page = reverse_lazy("todo:todo-list")
