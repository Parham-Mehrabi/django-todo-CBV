from django.views.generic import TemplateView


class TestWeatherView(TemplateView):
    template_name = 'weather/test.html'
