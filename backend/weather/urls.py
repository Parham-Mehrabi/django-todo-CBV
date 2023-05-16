from django.urls import path, include
from .views import TestWeatherView
app_name = 'weather'

urlpatterns = [
    path('api/v1/', include('weather.api.v1.urls', namespace='api-v1'), name='api-v1'),
    path('test/', TestWeatherView.as_view(), name='test'),
]
