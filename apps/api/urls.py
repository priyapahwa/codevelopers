from django.urls import include
from django.urls import path

from apps.api import views

urlpatterns = [
    path("users/", views.UserList.as_view(), name="api"),
    path("dj-rest-auth/", include("dj_rest_auth.urls")),
    path("dj-rest-auth/registration/", include("dj_rest_auth.registration.urls")),
    path("users/<int:id>", views.GenericUserAPIView.as_view()),
    path("register/", views.CustomRegisterView.as_view()),
    path("run/python3/", views.Python3.as_view()),
    path("run/python2/", views.Python2.as_view()),
    path("run/cpp/", views.CppCompiler.as_view()),
    path("run/c/", views.CCompiler.as_view()),
    path("run/java/", views.JavaCompiler.as_view()),
    
    
]
