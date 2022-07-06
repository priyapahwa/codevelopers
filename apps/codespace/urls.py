from django.urls import path

from apps.codespace.views import codeView
from apps.codespace.views import run_code
urlpatterns = [
    path("", codeView, name="codeview"),
    path("run/", run_code, name="codeview"),
]
