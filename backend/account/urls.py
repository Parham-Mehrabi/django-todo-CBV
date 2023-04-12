from django.urls import path
from .views import TodoLogoutView


app_name = 'account'

urlpatterns = [
    path('logout/', TodoLogoutView.as_view(), name='logout')
]