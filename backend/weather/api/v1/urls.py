from django.urls import path
from .views import GetTodayWeather


urlpatterns = [
    path('today/<str:city>/', GetTodayWeather.as_view(), name='today'),
]
