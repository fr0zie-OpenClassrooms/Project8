from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail, BadHeaderError
from django.db.models.query_utils import Q
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from .forms import RegistrationForm, PasswordResetForm
from .models import User


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
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.add_message(request, messages.SUCCESS, "Vous êtes connecté !")
            return redirect("account")
        else:
            messages.add_message(
                request, messages.ERROR, "Les champs renseignés sont invalides."
            )
            return render(request, "account/login.html", status=400)

    return render(request, "account/login.html")


def user_logout(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, "Vous êtes déconnecté !")
    return redirect("login")


def reset_password(request):
    form = PasswordResetForm()

    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        email = request.POST.get("email")
        associated_users = User.objects.filter(Q(email=email))
        if associated_users.exists():
            for user in associated_users:
                print(user.email)
                subject = "Demande de réinitialisation de mot de passe"
                email_template_name = "account/reset_email.txt"
                c = {
                    "email": user.email,
                    "domain": "127.0.0.1:8000",
                    "site_name": "Pur Beurre",
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "user": user,
                    "token": default_token_generator.make_token(user),
                    "protocol": "http",
                }
                email = render_to_string(email_template_name, c)

                try:
                    send_mail(
                        subject,
                        email,
                        "admin@example.com",
                        [user.email],
                        fail_silently=False,
                    )
                except BadHeaderError:
                    return HttpResponse("Invalid header found.")
                return redirect("done/")

    context = {"form": form}
    return render(request, "account/reset_password.html", context)


def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect("complete/")
    else:
        form = PasswordChangeForm(request.user)

    context = {"form": form}
    return render(request, "account/change_password.html", context)


def change_password_complete(request):
    return render(request, "account/reset_complete.html")
