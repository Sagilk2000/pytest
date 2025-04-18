from  rest_framework import serializers
from user import serializer as user_serializer
from . import services



class StatusSerializer(serializers.Serializer):
    """
        Serializer for the Status model or StatusDataClass.
        This class is responsible for converting complex data such as model instances
        into native Python datatypes that can then be easily rendered into JSON or other content types.

        Fields:
            id (IntegerField): Unique identifier for the status post. Read-only.
            content (CharField): The text content of the status post.
            date_published (DateTimeField): The timestamp when the status was created. Read-only.
            user (UserSerializer): Nested serializer representing the user who created the status. Read-only.
        """
    id = serializers.IntegerField(read_only=True)
    content = serializers.CharField()
    date_published = serializers.DateTimeField(read_only=True)
    user = user_serializer.UserSerializer(read_only=True)

    def to_internal_value(self, data):
        """
                Convert incoming primitive data into a validated internal data format.
                Overrides the default to transform the data into a custom StatusDataClass
                for further service-layer processing.

                Args:
                    data (dict): The incoming request data.

                Returns:
                    StatusDataClass: A dataclass instance with validated data.
                """
        data = super().to_internal_value(data)

        return services.StatusDataClass(**data)

    def to_representation(self, instance):
        """
                Convert the internal representation (e.g. StatusDataClass or model instance)
                into a native Python datatype for rendering.

                Args:
                    instance (StatusDataClass or model): The status instance to serialize.

                Returns:
                    dict: A serialized representation of the status data.
                """
        return {
            "id": instance.id,
            "content": instance.content,
            "date_published": instance.date_published,
            "user": user_serializer.UserSerializer(instance.user).data if instance.user else None
        }