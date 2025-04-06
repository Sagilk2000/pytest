from django.conf import settings
from rest_framework import authentication, exceptions
import jwt

from . import models

class CustomUserAuthentication(authentication.BaseAuthentication):
    """
        Custom authentication class that uses JWT tokens stored in cookies.

        This authentication method checks for a JWT token in the request cookies,
        decodes it using the project's secret key, and authenticates the user.
        """
    def authenticate(self, request):
        """
                Authenticate the user based on the JWT token from cookies.

                Args:
                    request: The incoming HTTP request.

                Returns:
                    A tuple of (user, None) if authentication is successful.
                    Returns None if no token is found.
                    Raises AuthenticationFailed if the token is invalid or user is not found.
                """
        token = request.COOKIES.get("jwt")

        if not token:
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        except:
            raise exceptions.AuthenticationFailed("Unauthorized")

        user = models.User.objects.filter(id=payload["id"]).first()

        return (user, None)

