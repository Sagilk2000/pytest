import dataclasses
import datetime
import jwt
from typing import TYPE_CHECKING
from django.conf import settings
from . import models
if TYPE_CHECKING:
    from models import User
@dataclasses.dataclass
class UserDataClass:
    """
        A data class representing a user.

        This class is used to create and manipulate user data
        without directly interacting with the database models.
        """
    first_name: str
    last_name: str
    email: str
    password: str=None
    id: int=None

    @classmethod
    def from_instance(cls, user: "User") -> "UserDataClass":
        """
                Create a UserDataClass instance from a User model instance.

                Args:
                    user (models.User): A User model instance.

                Returns:
                    UserDataClass: A new instance of UserDataClass.
                """
        return cls(
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            id=user.id
        )

def create_user(user_dc: "UserDataClass") -> "UserDataClass":
    """
        Create a new user in the database.

        Args:
            user_dc (UserDataClass): A data class containing user details.

        Returns:
            UserDataClass: A new instance with the saved user data.
        """
    instance = models.User(
        first_name=user_dc.first_name,
        last_name=user_dc.last_name,
        email=user_dc.email
    )
    if user_dc.password is not None:
        instance.set_password(user_dc.password)

    instance.save()

    return UserDataClass.from_instance(instance)

def user_email_selector(email: str) -> "User":
    """
        Retrieve a user from the database by email.

        Args:
            email (str): The email address of the user.

        Returns:
            models.User: The user instance if found, otherwise None.
        """
    user = models.User.objects.filter(email=email).first()

    return user

def crete_token(user_id: int) -> str:
    """
        Generate a JWT token for user authentication.

        Args:
            user_id (int): The ID of the user for whom the token is generated.

        Returns:
            str: A JWT token string.
        """
    payload = dict(
        id=user_id,
        exp=datetime.datetime.utcnow() + datetime.timedelta(hours=24),
        iat=datetime.datetime.utcnow()
    )
    token = jwt.encode(payload, settings.JWT_SECRET, algorithm="HS256")

    return token