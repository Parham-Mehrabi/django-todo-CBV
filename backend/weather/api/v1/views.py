import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class GetTodayWeather(APIView):
    """
        get today weather info from 'https://www.weatherapi.com/'
    """

    @method_decorator(cache_page(20 * 60, key_prefix='daily_weather'))
    def get(self, request, city, *args, **kwargs):
        url = f'https://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_TOKEN}&q={city}&aqi=yes'
        response = requests.get(url).json()
        return Response(response)


# method 2 :
'''
from django.core.cache import cache
class GetTodayWeather(APIView):
    """
        get today weather info from 'https://www.weatherapi.com/'
    """

    def get(self, request, city, *args, **kwargs):
        if cache.get(f'weather_response_cache_for_{city}') is None:
            url = f'http://api.weatherapi.com/v1/current.json?key={settings.WEATHER_API_TOKEN}&q={city}&aqi=yes'
            response = requests.get(url).json()
            cache.set(f'weather_response_cache_for_{city}', response, 20*60)
            return Response(response)
        return Response(cache.get('weather_response_cache'))
'''
