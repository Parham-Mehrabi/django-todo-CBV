from django.urls import path
from .views import TodoLogoutView, TodoRegisterView


app_name = 'account'

urlpatterns = [
    path('logout/', TodoLogoutView.as_view(), name='logout'),
    path('register/', TodoRegisterView.as_view(), name='register'),
]