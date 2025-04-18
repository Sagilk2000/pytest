from django.urls import path
from . import views

urlpatterns = [
    path("status/", views.StatusCreateListApi.as_view(), name="status"),
    path("status/<int:status_id>/", views.StatusRetrieveUpdateDelete.as_view(), name="status_detail")

]