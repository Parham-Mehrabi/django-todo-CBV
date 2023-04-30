from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from rest_framework.authtoken.views import ObtainAuthToken
from .views import RegisterApiView


urlpatterns = [

    # Register
    path('register/', RegisterApiView.as_view(), name='register_api'),



    # JWT:
    path('jwt/token/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/token/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

    # TOKEN:
    path('token/obtain', ObtainAuthToken.as_view(), name='token_obtain'),
]
