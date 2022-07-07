from rest_framework import serializers

from apps.accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            "id",
            "username",
        )
        model = CustomUser
