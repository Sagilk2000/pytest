from django.urls import path

from . import views

urlpatterns = [
    path("register/", views.RegisterApi.as_view(), name="register"),
    path("login/", views.LoginApi.as_view(), name="login"),
]
