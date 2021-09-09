from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Pseudonyme"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
            "password1": forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
            "password2": forms.PasswordInput(
                attrs={"placeholder": "Répéter le mot de passe"}
            ),
        }
        fields = ["username", "email", "password1", "password2"]
