import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings


class GetTodayWeather(APIView):
    """
        get today weather info from 'https://www.weatherapi.com/'
    """

    def get(self, request, city, *args, **kwargs):
        url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_TOKEN}&q={city}&aqi=yes'
        response = requests.get(url).json()
        return Response(response)
