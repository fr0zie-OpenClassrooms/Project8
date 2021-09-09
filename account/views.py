from django.contrib import auth
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import RegistrationForm


@login_required(login_url="login")
def index(request):
    return render(request, "account/index.html")


def user_register(request):
    form = RegistrationForm()

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {"form": form}
    return render(request, "account/register.html", context)


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("account")

    context = {}
    return render(request, "account/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")
