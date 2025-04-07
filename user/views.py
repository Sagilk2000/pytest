from django.shortcuts import render
from rest_framework import views, response, exceptions, permissions
from . import serializer as user_serializer

class RegisterApi(views.APIView):

    def post(self, request):
        serializer = user_serializer.UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        print(data)

        return response.Response(data={"hello": "world"})