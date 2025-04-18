import pytest
from rest_framework.test import APIClient

# Test user registration endpoint
@pytest.mark.django_db
def test_register_user(client):
    # Payload to register a new user
    payload = dict(
        first_name="sagil",
        last_name="k",
        email="sagil@gmail.com",
        password="timeforsometesting"
    )

    # Send POST request to /api/register/
    response = client.post("/api/register/", payload)
    data = response.data

    # Validate response data
    assert data["first_name"] == payload["first_name"]
    assert data["last_name"] == payload["last_name"]
    assert "password" not in data  # Password should not be exposed in response
    assert data["email"] == payload["email"]


# Test successful login with correct credentials
@pytest.mark.django_db
def test_login_user(user, client):
    # Send POST request to /api/login/ with valid credentials
    response = client.post("/api/login/", dict(email="sagil@gmail.com", password="ilovemagic"))

    # Assert login is successful
    assert response.status_code == 200


# Test login failure with incorrect credentials
@pytest.mark.django_db
def test_login_user_fail(client):
    # Send POST request with wrong credentials
    response = client.post("/api/login/", dict(email="sarangi@gmail.com", password="tknknometesting"))

    # Assert forbidden response
    assert response.status_code == 403


# Test retrieving the current authenticated user's data
@pytest.mark.django_db
def test_get_me(user, auth_client):
    # Send GET request to /api/me/ endpoint
    response = auth_client.get("/api/me/")

    # Assert user details are returned correctly
    assert response.status_code == 200
    data = response.data
    assert data["id"] == user.id
    assert data["email"] == user.email


# Test logout functionality for authenticated users
@pytest.mark.django_db
def test_logout(auth_client):
    # Send POST request to logout endpoint
    response = auth_client.post("/api/logout/")

    # Assert successful logout message
    assert response.status_code == 200
    assert response.data["message"] == "so long farewell"
