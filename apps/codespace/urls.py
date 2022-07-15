from django.urls import path

from apps.codespace.views import code_collab

# from apps.codespace.views import run_code

urlpatterns = [
    # path("", code_view, name="codeview"),
    path("<str:room_name>/", code_collab, name="code_collab")
    # path("run/", run_code, name="codeview"),
]
