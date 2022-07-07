import json
import sys
from io import StringIO

from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def code_view(request):
    return render(request, "codeview.html")


@csrf_exempt
def run_code(request):
    if request.method == "POST":
        body = json.loads(request.body)
        code = body["code"]
        print(code)
        # TODO (this is very unsafe way of executing untrusted scripts)
        out = StringIO()
        sys.stdout = out
        try:
            exec(code)
            results = out.getvalue()
            return JsonResponse(
                {"code": 0, "msg": "Successfully ran code", "results": results},
                status=200,
            )
        except:
            return JsonResponse(
                {"code": 1, "msg": "Could not execute the code"}, status=400
            )
