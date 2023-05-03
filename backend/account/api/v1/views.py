from rest_framework.generics import GenericAPIView, RetrieveUpdateAPIView
from .serializers import RegistrationSerializer, CostumeAuthTokenSerializer, ChangePasswordSerializer, ProfileSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken, Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()


class RegisterApiView(GenericAPIView):
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            data = {
                'email': serializer.data['email'],
                'message': 'user created successfully'
            }
            return Response(data, status=status.HTTP_201_CREATED)


class TokenLoginApi(ObtainAuthToken):
    """
        create or retrieve a token for user if username and password match.
    """
    serializer_class = CostumeAuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email
        })


class TokenLogoutApi(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ChangePasswordApiView(GenericAPIView):
    """
        an endpoint to change password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    # permission_classes = [IsAuthenticated]

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()     # NOQA
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                return Response({'old_password': ['wrong_password']}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get('new_password'))
            self.object.save()
            return Response({'details': 'password changed successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)
        return obj

    # def get_queryset(self):
    #     data = get_object_or_404(User, id=self.request.user.id)
    #     return data
