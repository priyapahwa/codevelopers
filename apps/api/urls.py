from django.urls import path

from apps.api import views

urlpatterns = [
    path("", views.UserList.as_view(), name="api"),
]
