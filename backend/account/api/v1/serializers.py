from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):

    password1 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password1']

    def validate(self, data):
        password = data.get('password')
        if password != data.get('password1'):
            raise serializers.ValidationError({'detail': 'passwords are not match'})

        user = User(email=data.get('email'), password=password)
        try:
            validate_password(password=password, user=user)
            # we pass a user object to validators to check if the username is too similar to password
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'password': e.messages})

        return super().validate(data)

    def create(self, validated_data):
        validated_data.pop('password1', None)
        return User.objects.create_user(**validated_data)
