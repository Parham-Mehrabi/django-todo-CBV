from django.urls import path, include
from .views import TodoLogoutView, TodoRegisterView


app_name = 'account'

urlpatterns = [
    path('logout/', TodoLogoutView.as_view(), name='logout'),
    path('register/', TodoRegisterView.as_view(), name='register'),
    path('api/v1/', include('account.api.v1.urls'), name='api-v1'),
]
