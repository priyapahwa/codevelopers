import imp

from django.urls import re_path

from apps.codespace.consumers import CodeCollabConsumer

websocket_urlpatterns = [
    re_path(r"ws/code/(?P<room_name>\w+)/$", CodeCollabConsumer.as_asgi()),
]
