from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput, PasswordInput, CheckboxInput


class CreateNewUserForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=False, label="Super Usuário", widget=CheckboxInput(attrs={"class":"form-check-control"}))

    password1 = forms.CharField(label=("Senha"), strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control"}),)
    
    password2 = forms.CharField(label=("Confirmar Senha"), strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password","class": "form-control"}),
    )


    class Meta:
        model = User

        fields = ["username", "password1", "password2", "is_superuser"]
        widgets = {
            "username": TextInput(attrs={"class": "form-control"}),
            }

