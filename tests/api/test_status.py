import pytest
from status import models

#  Test to ensure a new status can be created by an authenticated user
@pytest.mark.django_db
def test_create_status(auth_client, user):
    payload = dict(
        content="this is a really cool test. i love tests lol"
    )

    # Send POST request to create status
    response = auth_client.post("/api/status/", payload)
    data = response.data

    # Fetch status from database
    status_from_db = models.Status.objects.all().first()

    # Assert content and user match
    assert data["content"] == status_from_db.content
    assert data["id"] == status_from_db.id
    assert data["user"]["id"] == user.id


#  Test to ensure all statuses created by the authenticated user are returned
@pytest.mark.django_db
def test_get_user_status(auth_client, user):
    # Create multiple statuses for the user
    models.Status.objects.create(user_id=user.id, content="another test status")
    models.Status.objects.create(user_id=user.id, content="i love python, python is magical")

    # Send GET request to fetch user's statuses
    response = auth_client.get("/api/status/")

    # Assert response is successful and contains 2 items
    assert response.status_code == 200
    assert len(response.data) == 2


# Test to fetch the details of a specific status by ID
@pytest.mark.django_db
def test_get_user_status_detail(auth_client, user):
    # Create a status
    status = models.Status.objects.create(user_id=user.id, content="another test status")

    # Send GET request to fetch the specific status
    response = auth_client.get(f"/api/status/{status.id}/")

    # Assert correct status is returned
    assert response.status_code == 200
    data = response.data
    assert data["id"] == status.id
    assert data["content"] == status.content


#  Test to ensure a 404 response is returned for a non-existent status
@pytest.mark.django_db
def test_get_user_status_detail_404(auth_client):
    # Send GET request for a status ID that does not exist
    response = auth_client.get("/api/status/0/")
    assert response.status_code == 404


#  Test to update the content of a status
@pytest.mark.django_db
def test_put_user_status(auth_client, user):
    # Create a status
    status = models.Status.objects.create(user_id=user.id, content="another test status")

    # Payload with updated content
    payload = dict(content="i just update my status")

    # Send PUT request to update the status
    response = auth_client.put(f"/api/status/{status.id}/", payload)

    # Refresh from DB and assert the update was successful
    status.refresh_from_db()
    data = response.data

    assert data["id"] == status.id
    assert status.content == payload["content"]


# Test to delete a status and confirm it is removed from the database
@pytest.mark.django_db
def test_delete_user_status(auth_client, user):
    # Create a status
    status = models.Status.objects.create(user_id=user.id, content="another test status")

    # Send DELETE request
    response = auth_client.delete(f"/api/status/{status.id}/")

    # Assert successful deletion
    assert response.status_code == 204

    # Check that the status no longer exists
    with pytest.raises(models.Status.DoesNotExist):
        status.refresh_from_db()
