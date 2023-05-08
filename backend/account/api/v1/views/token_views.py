from rest_framework.authtoken.views import ObtainAuthToken, Token
from ..serializers import CostumeAuthTokenSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


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
    """
        this endpoint destroys user's Token from DataBase.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):        # noqa
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

