from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import TextInput, CheckboxInput


class CreateNewUserForm(UserCreationForm):
    password1 = forms.CharField(label=("Senha"), strip=False,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),)

    password2 = forms.CharField(label=("Confirmar Senha"), strip=False,
                                widget=forms.PasswordInput(attrs={"autocomplete": "new-password", "class": "form-control"}),)

    class Meta:
        model = User

        fields = ["username", "password1", "password2", "is_superuser"]
        widgets = {
            "username": TextInput(attrs={"class": "form-control"}),
        }
        error_messages = {
            "username": {
                "required": "O nome de usuário é obrigatório.",
                "unique": "Este nome de usuário já está em uso.",
                "max_length": "O nome de usuário não pode exceder 150 caracteres.",
            },
            "password1": {
                "required": "Você precisa informar uma senha.",
                "min_length": "A senha deve ter pelo menos 8 caracteres.",
            },
            "password2": {
                "required": "Você precisa confirmar a senha.",
                "password_mismatch": "As senhas não coincidem.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["is_superuser"].widget = CheckboxInput(attrs={"class": "form-check-input"})
        self.fields["is_superuser"].label = "Super Usuário"
        self.fields["is_superuser"].required = False


class LoginUserForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Credenciais inválidas. Por favor, tente novamente.",
        "inactive": "Esta conta está inativa.",
    }

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Usuário"}),
        label=("Usuário"),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Senha"}),
        label=("Senha"),
    )
