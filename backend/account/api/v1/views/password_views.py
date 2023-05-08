from ..serializers import ChangePasswordSerializer, ConfirmResetPasswordSerializer
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from ..serializers import ResetPasswordSerializer
from mail_templated import EmailMessage
from ...utils import EmailThread
import jwt
from django.conf import settings
from django.shortcuts import get_object_or_404

User = get_user_model()


class ChangePasswordApiView(GenericAPIView):
    """
    an endpoint to change password.
    """

    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()  # NOQA
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response(
                    {"old_password": ["wrong_password"]},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(
                {"details": "password changed successfully"}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordApi(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        token = serializer.validated_data["token"]
        user = serializer.validated_data["user"]
        email_obj = EmailMessage(
            "email/reset_password.tpl",
            {"token": token, "user": user},
            "parham-webdev@parham.com",
            to=[email],
        )
        EmailThread(email_obj).start()
        return Response({"success": "password rest link has been sent to your email"})


class ConfirmResetPasswordApi(GenericAPIView):
    """
    check the reset password token and set a new password
    """

    serializer_class = ConfirmResetPasswordSerializer

    def get(self, request, *args, **kwargs):
        return Response(
            {"details": "send new password via post request"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def post(self, request, token, *args, **kwargs):
        try:
            token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except jwt.exceptions.InvalidSignatureError:
            return Response({"details": "invalid token"})
        except jwt.exceptions.ExpiredSignatureError:
            return Response({"details": "token expired"})
        except jwt.DecodeError:
            return Response({"details": "invalid token"})
        except Exception as e:
            return Response(str(e))
        user = get_object_or_404(User, id=token.get("user_id"))
        serializer = ConfirmResetPasswordSerializer(
            data=request.data, context={"user": user}
        )
        # user sent to serializer for password validation
        serializer.is_valid(raise_exception=True)
        user.set_password(serializer.data.get("new_password"))
        user.save()
        return Response(
            {"details": "new password set to user successfully."},
            status=status.HTTP_200_OK,
        )
