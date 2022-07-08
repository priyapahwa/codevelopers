from dj_rest_auth.registration.views import RegisterView
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView
import json
import sys
from io import StringIO
import os
import subprocess
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from apps.accounts.models import CustomUser
from apps.api.serializers import UserSerializer
from codecs import encode

class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    model = CustomUser


class CustomRegisterView(RegisterView):
    queryset = CustomUser.objects.all()
    # model = CustomUser


class GenericUserAPIView(
    generics.GenericAPIView,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()
    model = CustomUser
    lookup_field = "id"

    def get(self, request, id=None):
        if id:
            return self.retrieve(request)
        else:
            return self.list(request)

    def post(self, request):
        return self.create(request)

    def put(self, request, id=None):
        return self.update(request, id)

    def delete(self, request, id=None):
        return self.destroy(request, id)


class CodeRunner(generics.GenericAPIView):
    @csrf_exempt
    def post(self, request):
        body = request.data["code"]
        try:
            input_data = encode(
            str(request.data["input"]).encode().decode("unicode_escape"),
            "raw_unicode_escape",
        )
            path = os.path.join(settings.BASE_DIR, "mediafiles", "python.py")
            destination = open(path, "w+")
            destination.write(body)
            destination.close()
            run = subprocess.Popen(
            ["python3.10", path],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            )
            grep_stdout = run.communicate(input=input_data)[0]
            return JsonResponse(
                {"code": 0, "msg": "Successfully ran code",'results':grep_stdout.decode()},
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )