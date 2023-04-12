from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('todo.urls', namespace='todo')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('auth/', include('account.urls', namespace='account'))
]


