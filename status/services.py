import dataclasses
import datetime
from unittest import SkipTest

from rest_framework import exceptions

from . import models as status_models
from user import services as user_services
from django.shortcuts import get_object_or_404

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .models import Status
    from user.models import User

@dataclasses.dataclass
class StatusDataClass:
    """
        A simple data class to represent status data in a decoupled, non-Django-model format.
        Useful for serializing/deserializing and separating business logic from Django ORM.

        Attributes:
            content (str): The text content of the status.
            date_published (datetime): Timestamp of when the status was created.
            user (UserDataClass): The user who posted the status.
            id (int): The unique ID of the status (if available).
        """
    content: str
    date_published: datetime.datetime = None
    user: user_services.UserDataClass = None
    id: int = None

    @classmethod
    def from_instance(cls, status_model: "Status") -> "StatusDataClass":
        """
                Convert a Django Status model instance into a StatusDataClass.

                Args:
                    status_model (Status): Django model instance.

                Returns:
                    StatusDataClass: A dataclass representation of the status.
                """
        return cls(
            content=status_model.content,
            date_published=status_model.date_published,
            id=status_model.id,
            user=status_model.user
        )

def create_status(user, status: "StatusDataClass") -> "StatusDataClass":
    """
        Create a new status for a given user.

        Args:
            user (User): The user creating the status.
            status (StatusDataClass): Data to create the status.

        Returns:
            StatusDataClass: The created status as a dataclass.
        """
    status_create = status_models.Status.objects.create(
        content=status.content,
        user=user
    )
    return StatusDataClass.from_instance(status_model=status_create)

def get_user_status(user: "User") -> list["StatusDataClass"]:
    """
        Fetch all statuses created by a given user.

        Args:
            user (User): The user whose statuses to fetch.

        Returns:
            List[StatusDataClass]: List of the user's statuses.
        """
    user_status = status_models.Status.objects.filter(user=user)

    return[StatusDataClass.from_instance(single_status) for single_status in user_status]

def get_user_status_detail(status_id: int) -> "StatusDataClass":
    """
        Retrieve a single status by ID.
        Args:
            status_id (int): The ID of the status.
        Returns:
            StatusDataClass: The status data."""


    status = get_object_or_404(status_models.Status, pk=status_id)

    return StatusDataClass.from_instance(status_model=status)



def delete_user_status(user: "User", status_id: int) -> "StatusDataClass":
    """
        Delete a status by ID if it belongs to the requesting user.

        Args:
            user (User): The user requesting the deletion.
            status_id (int): The ID of the status to delete.

        Raises:
            PermissionDenied: If the user is not the owner of the status.
        """

    status = get_object_or_404(status_models.Status, pk=status_id)
    if user.id != status.user.id:
        raise exceptions.PermissionDenied("you're not the user fool")
    status.delete()


def update_user_status(user: "User", status_id: int, status_data: "StatusDataClass"):
    """
        Update an existing status' content if it belongs to the user.

        Args:
            user (User): The user requesting the update.
            status_id (int): The ID of the status to update.
            status_data (StatusDataClass): The new status content.

        Raises:
            PermissionDenied: If the user does not own the status.

        Returns:
            StatusDataClass: The updated status as a dataclass.
        """

    status = get_object_or_404(status_models.Status, pk=status_id)
    if user.id != status.user.id:
        raise exceptions.PermissionDenied("you're not the user fool")

    status.content = status_data.content
    status.save()

    return StatusDataClass.from_instance(status_model=status)