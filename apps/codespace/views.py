import json
import sys
from io import StringIO

from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from apps.chat.models import ChatRoom
from apps.chat.models import ChatUser
from apps.chat.models import UserAndRoom
from apps.chat.views import is_room_occupied

# def code_view(request):
#     return render(request, "codeview.html")


@login_required
def code_collab(request, room_name):
    print(room_name, "visited")
    if not is_room_occupied(room_name):
        return render(
            request, "collab.html", {"room_name": room_name, "set_pass": True}
        )
    else:
        chat_user = ChatUser.objects.get(chat_user=request.user)
        print(chat_user)
        chat_rooms = UserAndRoom.objects.filter(chat_user=chat_user)
        print(chat_rooms)
        for room in chat_rooms:
            if str(room.chat_room) == room_name:
                return render(
                    request,
                    "collab.html",
                    {"room_name": room_name, "user": request.user},
                )
        return render(
            request,
            "collab.html",
            {
                "room_name": room_name,
                "get_pass": True,
            },
        )


# @csrf_exempt
# def run_code(request):
#     if request.method == "POST":
#         body = json.loads(request.body)
#         code = body["code"]
#         print(code)
#         # TODO (this is very unsafe way of executing untrusted scripts)
#         out = StringIO()
#         sys.stdout = out
#         try:
#             exec(code)
#             results = out.getvalue()
#             return JsonResponse(
#                 {"code": 0, "msg": "Successfully ran code", "results": results},
#                 status=200,
#             )
#         except:
#             return JsonResponse(
#                 {"code": 1, "msg": "Could not execute the code"}, status=400
#             )
