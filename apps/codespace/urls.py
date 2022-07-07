from django.urls import path

from apps.codespace.views import code_view
from apps.codespace.views import run_code

urlpatterns = [
    path("", code_view, name="codeview"),
    path("run/", run_code, name="codeview"),
]
