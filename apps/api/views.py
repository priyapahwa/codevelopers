import json
import os
import subprocess
import sys
from codecs import encode
from io import StringIO

from dj_rest_auth.registration.views import RegisterView
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import mixins
from rest_framework.views import APIView

from apps.accounts.models import CustomUser
from apps.api.serializers import UserSerializer


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


class Python2(generics.GenericAPIView):
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
                ["python2.7", path],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            grep_stdout = run.communicate(input=input_data)[0]
            return JsonResponse(
                {
                    "code": 0,
                    "msg": "Successfully ran code",
                    "results": grep_stdout.decode(),
                },
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )


class Python3(generics.GenericAPIView):
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
                {
                    "code": 0,
                    "msg": "Successfully ran code",
                    "results": grep_stdout.decode(),
                },
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )


class CppCompiler(generics.GenericAPIView):
    @csrf_exempt
    def post(self, request):
        body = request.data["code"]
        try:
            input_data = encode(
                str(request.data["input"]).encode().decode("unicode_escape"),
                "raw_unicode_escape",
            )
            path = os.path.join(settings.BASE_DIR, "mediafiles", "cpp.cpp")
            out = os.path.splitext(path)[0]
            destination = open(path, "w+")
            destination.write(body)
            destination.close()
            run = subprocess.Popen(
                ["c++", path, "-o", out],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            grep_stdout = run.communicate(input=input_data)[0]
            if run.returncode == 0:
                run2 = subprocess.Popen(
                    [out],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                grep_stdout2 = run2.communicate(input=input_data)[0]
                output = grep_stdout2.decode()
            else:
                output = grep_stdout.decode()
            return JsonResponse(
                {"code": 0, "msg": "Successfully ran code", "results": output},
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )


class CCompiler(generics.GenericAPIView):
    @csrf_exempt
    def post(self, request):
        body = request.data["code"]
        try:
            input_data = encode(
                str(request.data["input"]).encode().decode("unicode_escape"),
                "raw_unicode_escape",
            )
            path = os.path.join(settings.BASE_DIR, "mediafiles", "cpp.cpp")
            out = os.path.splitext(path)[0]
            destination = open(path, "w+")
            destination.write(body)
            destination.close()
            run = subprocess.Popen(
                ["cc", path, "-o", out],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            grep_stdout = run.communicate(input=input_data)[0]
            if run.returncode == 0:
                run2 = subprocess.Popen(
                    [out],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                grep_stdout2 = run2.communicate(input=input_data)[0]
                output = grep_stdout2.decode()
            else:
                output = grep_stdout.decode()
            return JsonResponse(
                {"code": 0, "msg": "Successfully ran code", "results": output},
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )


class JavaCompiler(generics.GenericAPIView):
    @csrf_exempt
    def post(self, request):
        body = request.data["code"]
        try:
            input_data = encode(
                str(request.data["input"]).encode().decode("unicode_escape"),
                "raw_unicode_escape",
            )
            path = os.path.join(settings.BASE_DIR, "mediafiles", "cpp.cpp")
            out = os.path.splitext(path)[0]
            destination = open(path, "w+")
            destination.write(body)
            destination.close()
            run = subprocess.Popen(
                ["javac11", path, "-d", out],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
            )
            grep_stdout = run.communicate(input=b"")[0]
            if run.returncode == 0:
                run2 = subprocess.Popen(
                    ["java11", "-cp", out, "Solution"],
                    stdin=subprocess.PIPE,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                )
                grep_stdout2 = run2.communicate(input=input_data)[0]
                output = grep_stdout2.decode()
            else:
                output = grep_stdout.decode()
            return JsonResponse(
                {"code": 0, "msg": "Successfully ran code", "results": output},
                status=200,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )
