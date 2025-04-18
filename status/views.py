from rest_framework import views
from rest_framework import response
from user import authentication
from rest_framework import permissions
from . import serializer as status_serializer
from . import services
from rest_framework import status

class StatusCreateListApi(views.APIView):
    """
        API View for authenticated users to:
        - POST: Create a new status.
        - GET: Retrieve a list of their own statuses.
        """
    authentication_classes = (authentication.CustomUserAuthentication, )
    permission_classes = (permissions.IsAuthenticated, )

    def post(self, request):
        """
                Create a new status post for the authenticated user.

                Steps:
                1. Validate the request data using StatusSerializer.
                2. Create the status using service logic.
                3. Return the serialized response.
                """
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        serializer.instance = services.create_status(user=request.user, status=data)

        return response.Response(data=serializer.data)

    def get(self, request):
        """
               Retrieve all status posts for the authenticated user.
               """
        status_collection = services.get_user_status(user=request.user)
        serializer = status_serializer.StatusSerializer(status_collection, many=True)

        return response.Response(data=serializer.data)



class StatusRetrieveUpdateDelete(views.APIView):
    """
        API View to:
        - GET: Retrieve a single status by ID.
        - PUT: Update an existing status (only if owned by the user).
        - DELETE: Delete a status (only if owned by the user).
        """
    authentication_classes = (authentication.CustomUserAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, status_id):
        """
                Retrieve a single status post by its ID.
                """
        status = services.get_user_status_detail(status_id=status_id)
        serializer = status_serializer.StatusSerializer(status)
        return response.Response(data=serializer.data)

    def delete(self, request, status_id):
        """
                Delete a status post by ID if the user owns it.
                """
        services.delete_user_status(user=request.user, status_id=status_id)
        return response.Response(status=status.HTTP_204_NO_CONTENT)

    def put(self, request, status_id):
        """
                Update a status post by ID if the user owns it.

                Steps:
                1. Validate incoming data.
                2. Update the existing status using the services layer.
                3. Return the updated data.
                """
        serializer = status_serializer.StatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        status = serializer.validated_data
        serializer.instance = services.update_user_status(user=request.user, status_id=status_id, status_data=status)

        return response.Response(data=serializer.data)






