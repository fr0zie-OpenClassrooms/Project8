from django.shortcuts import render


def index(request):
    return render(request, "home/index.html")


def legal(request):
    return render(request, "home/legal.html")


def not_found(request, exception=None):
    return render(request, "home/404.html")
