import pytest
from user import services as user_services
from rest_framework.test import APIClient

# Fixture to create a test user using your service layer
@pytest.fixture
def user():
    user_dc = user_services.UserDataClass(
        first_name="sagil",
        last_name="k",
        email="sagil@gmail.com",
        password="ilovemagic"
    )
    user = user_services.create_user(user_dc=user_dc)
    return user

# Fixture to return a new instance of DRF's APIClient
@pytest.fixture
def client():
    return APIClient()

# Fixture that logs in the test user and returns an authenticated client
@pytest.fixture
def auth_client(user, client):
    client.post("/api/login/", dict(email=user.email, password="ilovemagic"))
    return client
