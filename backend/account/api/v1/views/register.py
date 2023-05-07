from ..serializers import RegistrationSerializer, ActivationResendSerializer
from rest_framework import status
from rest_framework.response import Response
from mail_templated import EmailMessage
from rest_framework.generics import GenericAPIView
from ...utils import EmailThread
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
import jwt
from django.conf import settings

User = get_user_model()


class RegisterApiView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):  # noqa
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data["email"]
            serializer.save()
            user_obj = get_object_or_404(User, email=email)
            token = self.get_token_for_user(user=user_obj)

            email_obj = EmailMessage(
                "email/activation_email.tpl",
                {"token": token},
                "parham-webdev@parham.com",
                to=[email],
            )
            EmailThread(email_obj).start()
            data = {
                "email": serializer.data["email"],
                "message": "user created successfully",
                "verify": "activation email has been sent",
            }
            return Response(data, status=status.HTTP_201_CREATED)

    def get_token_for_user(self, user):  # noqa
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)


class VerifyEmail(APIView):
    """
    verify user's email
    """

    def get(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        except jwt.exceptions.ExpiredSignatureError:
            return Response({"details": "token expired"})
        except jwt.exceptions.InvalidSignatureError:
            return Response({"details": "invalid token"})
        except jwt.DecodeError:
            return Response({"details": "invalid token"})
        except Exception as e:
            return Response(str(e))

        user_id = token.get("user_id")
        user_obj = User.objects.get(id=user_id)
        if user_obj.is_verified:
            return Response({"details": "your account is already verified"})
        user_obj.is_verified = True
        user_obj.save()

        return Response(
            {"details": "your account has been verified successfully. "},
            status=status.HTTP_202_ACCEPTED,
        )


class ResendVerifyEmail(GenericAPIView):
    serializer_class = ActivationResendSerializer

    def post(self, request, *args, **kwargs):
        serializer = ActivationResendSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        email = serializer.validated_data["email"]
        token = self.get_token_for_user(user=user)
        email_obj = EmailMessage(
            "email/activation_email.tpl",
            {"token": token},
            "parham-webdev@parham.com",
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response(
            {"details": "user activation resend successfully"}, status.HTTP_200_OK
        )

    def get_token_for_user(self, user):  # noqa
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
