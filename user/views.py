from django.shortcuts import render
from rest_framework import views, response, exceptions, permissions
from . import serializer as user_serializer
from . import services

class RegisterApi(views.APIView):
    """
       API endpoint for user registration.

       This endpoint allows new users to register by providing their details.
       """

    def post(self, request):
        """
                Handle POST requests for user registration.

                Args:
                    request: The HTTP request object containing user registration data.

                Returns:
                    Response: A response containing the serialized user data.
                """
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        serializer.instance = services.create_user(user_dc=data)

        print(data)

        return response.Response(data=serializer.data)


class LoginApi(views.APIView):
    """
        API endpoint for user authentication (login).

        This endpoint verifies user credentials and returns a JWT token.
        """
    def post(self, request):
        """
                Handle POST requests for user login.

                Args:
                    request: The HTTP request object containing login credentials.

                Returns:
                    Response: A response containing the authentication token.
                """
        email = request.data.get("email")
        password = request.data.get("password")

        user = services.user_email_selector(email=email)

        if user is None:
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        if not user.check_password(raw_password=password):
            raise exceptions.AuthenticationFailed("Invalid Credentials")

        token = services.crete_token(user_id=user.id)

        resp = response.Response()

        resp.set_cookie(key="jwt", value=token, httponly=True)

        return resp

# {
# "email": "sanath@gmail.com",
# "password": "Sanath@123"
# }

# {
#     "first_name": "sarang",
#     "last_name": "km",
#     "email": "sarang@gmail.com",
#     "password": "Sarang@123"
# }