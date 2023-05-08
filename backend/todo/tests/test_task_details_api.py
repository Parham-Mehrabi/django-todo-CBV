import pytest
from django.urls import reverse
from todo.models import Task


@pytest.mark.django_db
class TestTaskDetailsApi:
    """
    test task details api views' responses
    """

    def test_get_task_details_verified_user(
        self, api_client, verified_user, user_task, user0_task, user0
    ):
        """a verified user try to get details for its own task, someone else's task and a non-exist task"""

        # user's task
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user_task.id})
        api_client.force_authenticate(verified_user)
        response = api_client.get(url)
        assert response.status_code == 200

        # someone else's task
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user0_task.id})
        response = api_client.get(url)
        assert response.status_code == 404

        # not exist task
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": 0})
        response = api_client.get(url)
        assert response.status_code == 404

    def test_get_task_details_unverified_user_403(
        self, api_client, unverified_user, unverified_user_task, user0_task, user0
    ):
        """a verified user try to get details for its own task, someone else's task and a non-exist task"""

        # user's task
        url = reverse(
            "todo:api-v1:tasks-detail", kwargs={"pk": unverified_user_task.id}
        )
        api_client.force_authenticate(unverified_user)
        response = api_client.get(url)
        assert response.status_code == 403
        # someone else's task
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user0_task.id})
        response = api_client.get(url)
        assert response.status_code == 403

        # not exist task
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": 0})
        response = api_client.get(url)
        assert response.status_code == 403

    def test_get_task_details_unauthorized_user_401(self, api_client):
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": 0})
        response = api_client.get(url)
        assert response.status_code == 401


@pytest.mark.django_db
class TestTaskDetailsDeletePutPatchApi:
    """
    test other methods (put, delete, patch) on task details
    """

    def test_put_patch_task_api(self, api_client, verified_user, user_task):
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user_task.id})
        api_client.force_authenticate(verified_user)
        data = {
            "title": "put_task_title",
            "context": "put_task_context",
            "is_complete": True,
        }
        response = api_client.put(url, data=data)
        assert response.status_code == 200
        try:
            Task.objects.get(
                title="put_task_title", context="put_task_context", is_complete=True
            )
            assert True
        except Task.DoesNotExist:
            assert False
        patch_data = {
            "title": "patch_task_title",
        }
        response = api_client.patch(url, data=patch_data)
        assert response.status_code == 200
        try:
            Task.objects.get(
                title="patch_task_title", context="put_task_context", is_complete=True
            )
            assert True
        except Task.DoesNotExist:
            assert False

    def test_delete_task_api(self, api_client, verified_user, user_task):
        """delete a task with a verified user"""
        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user_task.id})
        api_client.force_authenticate(verified_user)
        response = api_client.delete(url)
        assert response.status_code == 204

    def test_delete_task_api_unauthorized(self, api_client, user0_task):
        """try to delete a task without authorization"""

        url = reverse("todo:api-v1:tasks-detail", kwargs={"pk": user0_task.id})
        response = api_client.delete(url)
        assert response.status_code == 401

    def test_delete_task_api_unverified(
        self, api_client, unverified_user_task, unverified_user
    ):
        """try to delete a task with an unverified user"""
        url = reverse(
            "todo:api-v1:tasks-detail", kwargs={"pk": unverified_user_task.id}
        )
        api_client.force_authenticate(unverified_user)
        response = api_client.delete(url)
        assert response.status_code == 403

    def test_fail(self):
        assert False
