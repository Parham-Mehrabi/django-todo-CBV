from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import RegisterApiView, TokenLoginApi, TokenLogoutApi


urlpatterns = [

    # Register
    path('register/', RegisterApiView.as_view(), name='register_api'),

    # TOKEN:
    path('token/login/', TokenLoginApi.as_view(), name='token_login'),
    path('token/logout/', TokenLogoutApi.as_view(), name='token_logout'),


    # JWT:
    path('jwt/token/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'),
    path('jwt/token/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/token/verify/', TokenVerifyView.as_view(), name='jwt_verify'),

]
