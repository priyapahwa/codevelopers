from django.urls import path

from apps.chat import views

urlpatterns = [
    path("", views.index, name="index"),
    path("<str:room_name>/", views.room, name="room"),
    path("auth/", views.room_auth, name="room_auth"),
]
