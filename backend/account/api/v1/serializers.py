from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from todo.models import Task
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


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


class CostumeAuthTokenSerializer(serializers.Serializer):
    email = serializers.CharField(
        label=_("Email"),
        write_only=True
    )
    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )
    token = serializers.CharField(
        label=_("Token"),
        read_only=True
    )

    def validate(self, attrs):
        username = attrs.get('email')
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

        else:
            msg = _('Must include "username" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class ChangePasswordSerializer(serializers.Serializer):

    old_password = serializers.CharField(required=True, max_length=128)
    new_password = serializers.CharField(required=True, max_length=128)
    new_password1 = serializers.CharField(required=True, max_length=128)

    def validate(self, attrs):
        if attrs.get('new_password') != attrs.get('new_password1'):
            raise serializers.ValidationError({
                'detail': 'passwords doesnt match'
            })
        try:
            validate_password(attrs.get('new_password'))
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)


class ProfileSerializer(serializers.ModelSerializer):
    tasks_count = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ('email', 'tasks_count', 'is_staff', 'is_active', 'is_superuser', 'is_verified', 'created_date')
        read_only_fields = ['tasks_count', 'is_staff', 'is_active', 'is_superuser', 'is_verified']

    def get_tasks_count(self, obj):     # noqa
        return Task.objects.filter(author=obj).count()


class ActivationResendSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'details': 'user does not exist'})
        if user_obj.is_verified:
            raise serializers.ValidationError({'details': 'user is already verified'})
        attrs['user'] = user_obj

        return super().validate(attrs)


class ResetPasswordSerializer(serializers.Serializer):
    """
        check if the email exist and create a jwt token for user
    """
    email = serializers.EmailField(required=True)

    def validate(self, attrs):
        email = attrs.get('email')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'details': 'user does not exist'})
        refresh = RefreshToken.for_user(user)
        token = str(refresh.access_token)
        attrs['token'] = token
        attrs['user'] = user
        return super().validate(attrs)


class ConfirmResetPasswordSerializer(serializers.Serializer):

    new_password = serializers.CharField(max_length=128, required=True)
    new_password1 = serializers.CharField(max_length=128, required=True)

    def validate(self, attrs):
        password = attrs.get('new_password')
        if password != attrs.get('new_password1'):
            raise serializers.ValidationError({
                'detail': 'passwords doesnt match'
            })
        try:
            validate_password(password=attrs.get('new_password'), user=self.context.get('user'))
            # user passed to validation to check its similarity with email address
        except exceptions.ValidationError as e:
            raise serializers.ValidationError({'new_password': list(e.messages)})
        return super().validate(attrs)
