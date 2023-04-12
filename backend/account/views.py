from django.contrib.auth.views import LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin



class TodoLogoutView(LogoutView, LoginRequiredMixin):
    """
        Log out the user and redirect to login Page.
    """
    next_page = '/'
