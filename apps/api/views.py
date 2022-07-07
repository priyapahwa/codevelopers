from rest_framework import generics

from apps.accounts.models import CustomUser
from apps.api.serializers import UserSerializer


class UserList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
