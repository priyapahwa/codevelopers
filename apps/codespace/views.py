from django.shortcuts import render


def codeView(request):
    return render(request, "codeview.html")
