from django.urls import path

from apps.core.views import homePageView

urlpatterns = [
    path("", homePageView, name="home"),
]
