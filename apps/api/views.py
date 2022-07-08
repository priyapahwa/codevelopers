from dj_rest_auth.registration.views import RegisterView
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
