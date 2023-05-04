from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from ..views import (RegisterApiView, TokenLoginApi, TokenLogoutApi,
                     ChangePasswordApiView, VerifyEmail, ResendVerifyEmail,
                     ResetPasswordApi, ConfirmResetPasswordApi)


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
    path('reset-password/', ResetPasswordApi.as_view(), name='reset_password'),
    path('reset-password/confirm/<str:token>', ConfirmResetPasswordApi.as_view(), name='reset_password_confirm'),

    # activation
    path('activation/confirm/<str:token>', VerifyEmail.as_view(), name='email_verification'),
    path('activation/resend/', ResendVerifyEmail.as_view(), name='email_verification_resend'),

]
