from django.urls import path
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path("", views.index, name="account"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    path("reset/", views.reset_password, name="password_reset"),
    path(
        "reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="account/reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="account/reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/complete/",
        views.change_password_complete,
        name="password_reset_complete",
    ),
    path("edit/", views.change_password, name="password_change"),
    path(
        "edit/complete/",
        views.change_password_complete,
        name="password_change_complete",
    ),
]
