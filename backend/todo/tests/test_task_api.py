import pytest
from django.urls import reverse
from todo.tests.fixtures import (api_client, verified_user, unverified_user,            # noqa
                                 user0, user_task, user0_task, unverified_user_task)    # noqa
from todo.models import Task


@pytest.mark.django_db
class TestTaskListApiResponses:
    """
        test task list api views' responses
    """

    # get:
    def test_get_task_unauthorized_status_401(self, api_client):
        """ try to get task_list without authorization """
        url = reverse('todo:api-v1:tasks-list')
        response = api_client.get(url)
        assert response.status_code == 401

    def test_get_task_authorized_verified_status_200(self, api_client, verified_user):
        """ try to get task_list as a verified user """
        url = reverse('todo:api-v1:tasks-list')
        api_client.force_authenticate(verified_user)
        response = api_client.get(url)
        assert response.status_code == 200

    def test_get_task_authorized_unverified_status_403(self, api_client, unverified_user):
        """ try to get task_list as an unverified user """
        url = reverse('todo:api-v1:tasks-list')
        api_client.force_authenticate(unverified_user)
        response = api_client.get(url)
        assert response.status_code == 403

    # post valid_data:
    def test_post_task_valid_data_unauthorized_401(self, api_client):
        """ try to post a new task without authorization """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "string",
            "context": "string",
            "is_complete": False
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 401

    def test_post_task_valid_data_unverified_403(self, api_client, unverified_user):
        """ try to post a new task without an unverified user """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "string",
            "context": "string",
            "is_complete": False
        }
        api_client.force_authenticate(unverified_user)
        response = api_client.post(url, data=data)
        assert response.status_code == 403

    def test_post_task_valid_data_verified_201(self, api_client, verified_user):
        """ try to post a new task with a verified user """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "string",
            "context": "test_post_task_valid_data_verified_201",
            "is_complete": False
        }
        api_client.force_authenticate(verified_user)
        response = api_client.post(url, data=data)
        assert response.status_code == 201
        try:
            Task.objects.get(
                title='string',
                context='test_post_task_valid_data_verified_201',
                author=verified_user
            )
            # Task creation verified in database
            assert True
        except Task.DoesNotExist:
            # Task do not created
            assert False

    # post invalid_data:
    def test_post_task_invalid_data_unauthorized_401(self, api_client):
        """ try to post a new task without authorization and invalid data """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "",
            "context": "string",
            "is_complete": False
        }
        response = api_client.post(url, data=data)
        assert response.status_code == 401

    def test_post_task_invalid_data_unverified_403(self, api_client, unverified_user):
        """ try to post a new task without an unverified user and invalid data """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "",
            "context": "string",
            "is_complete": False
        }
        api_client.force_authenticate(unverified_user)
        response = api_client.post(url, data=data)
        assert response.status_code == 403

    def test_post_task_invalid_data_verified_400(self, api_client, verified_user):
        """ try to post a new task with a verified user and invalid data """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "",
            "context": "string",
            "is_complete": True
        }
        api_client.force_authenticate(verified_user)
        response = api_client.post(url, data=data)
        assert response.status_code == 400

    def test_task_invalid_methods_405(self, api_client, verified_user, user_task):
        """ trying invalid request methods as a verified user """
        url = reverse('todo:api-v1:tasks-list')
        data = {
            "title": "invalid",
            "context": "string",
        }
        api_client.force_authenticate(verified_user)

        delete_request_status = api_client.delete(url).status_code
        patch_request_status = api_client.patch(url, data).status_code
        put_request_status = api_client.put(url, data).status_code

        assert delete_request_status == 405
        assert patch_request_status == 405
        assert put_request_status == 405
