from django.urls import path

from apps.codespace.views import codeView

urlpatterns = [
    path("", codeView, name="codeview"),
]
