from rest_framework.generics import GenericAPIView
from .serializers import RegistrationSerializer
from rest_framework import status
from rest_framework.response import Response


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
