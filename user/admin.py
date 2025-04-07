from django.contrib import admin
from . import models
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    """
        Custom admin interface for the User model.

        This class defines how the User model will be displayed in the Django admin panel.
        """
    list_display = (
        "id",
        "first_name",
        "last_name",
        "email"
    )

admin.site.register(models.User, UserAdmin)