import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from todo.models import Task

User = get_user_model()


@pytest.fixture
def api_client():
    client = APIClient()
    return client


@pytest.fixture
def verified_user():
    verified_user = User.objects.create_user(
        email="verifieduser@parham.com", password="parham654321", is_verified=True
    )
    return verified_user


@pytest.fixture
def unverified_user():
    unverified_user = User.objects.create_user(
        email="unverifieduser@parham.com", password="parham654321", is_verified=False
    )
    return unverified_user


@pytest.fixture
def user0():
    user0 = User.objects.create_user(
        email="user0@parham.com", password="parham654321", is_verified=True
    )
    return user0


@pytest.fixture
def user_task(verified_user):
    user_task = Task.objects.create(
        author=verified_user, title="test", context="test", is_complete=False
    )
    return user_task


@pytest.fixture
def unverified_user_task(unverified_user):
    unverified_user_task = Task.objects.create(
        author=unverified_user, title="test", context="test", is_complete=False
    )
    return unverified_user_task


@pytest.fixture
def user0_task(user0):
    user0_task = Task.objects.create(
        author=user0, title="test", context="test", is_complete=False
    )
    return user0_task
