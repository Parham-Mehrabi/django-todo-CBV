from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from ..views import RegisterApiView, TokenLoginApi, TokenLogoutApi, ChangePasswordApiView


urlpatterns = [

    # Register
    path('register/', RegisterApiView.as_view(), name='register_api'),

    # Login TOKEN:
    path('token/login/', TokenLoginApi.as_view(), name='token_login'),
    path('token/logout/', TokenLogoutApi.as_view(), name='token_logout'),


    # Login JWT:
    path('jwt/create/', TokenObtainPairView.as_view(), name='jwt_obtain_pair'),
    path('jwt/refresh/', TokenRefreshView.as_view(), name='jwt_refresh'),
    path('jwt/verify/', TokenVerifyView.as_view(), name='jwt_verify'),


    # change password
    path('change-password/', ChangePasswordApiView.as_view(), name='change_password'),

    # reset password

]
