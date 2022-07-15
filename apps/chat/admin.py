from django.contrib import admin

from apps.chat.models import ChatRoom
from apps.chat.models import ChatUser
from apps.chat.models import UserAndRoom

admin.site.register(ChatUser)
admin.site.register(ChatRoom)
admin.site.register(UserAndRoom)
