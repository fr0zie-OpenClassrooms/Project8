from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import User


class RegistrationForm(UserCreationForm):
    password1 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(attrs={"placeholder": "Mot de passe"}),
    )
    password2 = forms.CharField(
        max_length=16,
        widget=forms.PasswordInput(attrs={"placeholder": "Confirmez le mot de passe"}),
    )

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ("username", "email")
        widgets = {
            "username": forms.TextInput(attrs={"placeholder": "Pseudonyme"}),
            "email": forms.TextInput(attrs={"placeholder": "Email"}),
        }
