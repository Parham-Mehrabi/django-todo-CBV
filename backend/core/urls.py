from django.contrib import admin
from django.urls import path, include

# document
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Parham Todo API",
        default_version="v1",
        description="this api is for our useless todo app",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="parham.mehrabi.webdev@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("todo.urls", namespace="todo")),
    path("accounts/", include("django.contrib.auth.urls")),
    path("auth/", include("account.urls", namespace="account")),
    # documentation:
    path(
        "swagger/document.yml",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
