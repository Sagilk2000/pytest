from django.db import models
from django.conf import settings

class Status(models.Model):
    """
        Model representing a status update or post made by a user.

        Fields:
            user (ForeignKey): A reference to the user who created the status.
            When the user is deleted, all their statuses will be deleted as well (CASCADE).
            content (TextField): The textual content of the status post.
            date_published (DateTimeField): The date and time when the status was created.
            Automatically set to the current timestamp when the object is first created.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name="user"
    )

    content = models.TextField(
        verbose_name="content"
    )

    date_published = models.DateTimeField(auto_now_add=True, verbose_name="Date published")
