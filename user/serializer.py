from rest_framework import serializers
from . import services
class UserSerializer(serializers.Serializer):
    """
        Serializer for User model.
        This serializer is used to convert User model instances into JSON format
        and validate incoming data for user creation or updates.
        """
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    """
        Convert the input data to an internal Python representation.

        This method is overridden to transform validated data into a `UserDataClass`
        object before it is used in the application.

        Args:
             data ddict): The input data validated by the serializer.

        Returns:
                UserDataClass: An instance of UserDataClass containing user data."""
    def to_internal_value(self, data):
        data = super().to_internal_value(data)

        return services.UserDataClass(**data)