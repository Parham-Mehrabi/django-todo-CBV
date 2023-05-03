from rest_framework.generics import  RetrieveUpdateAPIView
from ..serializers import ProfileSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
User = get_user_model()


class ProfileApiView(RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = get_object_or_404(User, id=self.request.user.id)
        return obj

    # def get_queryset(self):
    #     data = get_object_or_404(User, id=self.request.user.id)
    #     return data
