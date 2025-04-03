from django.db import models
from django.contrib.auth import models as auth_models



class UserManager(auth_models.BaseUserManager):

     def create_user(self, first_name: str, last_name: str, email: str = None, password: str = None, is_staff=False, is_superuser=False ) ->"User":
         """
                Create and return a regular user with the given details.

                Args:
                    first_name (str): First name of the user.
                    last_name (str): Last name of the user.
                    email (str, optional): User's email address. Defaults to None.
                    password (str, optional): User's password. Defaults to None.
                    is_staff (bool, optional): Whether the user is staff. Defaults to False.
                    is_superuser (bool, optional): Whether the user is a superuser. Defaults to False.

                Raises:
                    ValueError: If email , first_name, or last_name is not provided.

                Returns:
                    User: The created user instance.
                """
         if not email:
             raise ValueError("User must have an email")
         if not first_name:
             raise ValueError("User must have an first_name")
         if not last_name:
             raise ValueError("User must have an last_name")

         user = self.model(email=self.normalize_email(email))
         user.first_name = first_name
         user.last_name = last_name
         user.set_password(password)
         user.is_active = True
         user.is_staff = is_staff
         user.is_superuser = is_superuser
         user.save()

         return user

     def create_superuser(self, first_name:str, last_name:str, email: str, password=str) -> "User":
         """
                 Create and return a superuser with the given details.

                 Args:
                     first_name (str): First name of the superuser.
                     last_name (str): Last name of the superuser.
                     email (str): Superuser's email address.
                     password (str): Superuser's password.

                 Returns:
                     User: The created superuser instance.
                 """
         user = self.create_user(
             first_name= first_name,
             last_name= last_name,
             email= email,
             password= password,
             is_staff= True,
             is_superuser= True

         )
         user.save()

         return user


class User(auth_models.AbstractUser):
    """
        Custom user model that uses email instead of username for authentication.

        This model extends Django's AbstractUser and removes the username field.
        """
    first_name = models.CharField(verbose_name="First Name", max_length=255)
    last_name = models.CharField(verbose_name="Last Name", max_length=255)
    email = models.EmailField(verbose_name="Email", max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]
