from django.urls import path
from .views import GetTodayWeather

app_name = 'weather_api'

urlpatterns = [
    path('today/<str:city>/', GetTodayWeather.as_view(), name='today'),
]
