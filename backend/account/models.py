from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _


class CostumeUserManager(BaseUserManager):
    """ costume user manager where email is the unique identifier """

    def create_user(self, email, password, **other):
        """ create user with an email and password and extra data """
        if not email:
            raise ValueError(_('email is requierd ! ! !'))
        email = self.normalize_email(email)
        user = self.model(email=email, **other)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **others):
        """ create the user but with is_superuser and is_staff set to True """

        others.setdefault('is_staff', True)
        others.setdefault('is_superuser', True)
        others.setdefault('is_active', True)

        if others.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        
        if others.get('is_active') is not True:
            raise ValueError(_('Superuser must have is_active=True.'))
        
        if others.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        self.create_user(email=email, password=password, **others)


class CostumUser(AbstractBaseUser, PermissionsMixin):
    """ costume user model for our app """

    email = models.EmailField(max_length=255, unique=True )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CostumeUserManager()

    def __str__(self):
        return self.email
