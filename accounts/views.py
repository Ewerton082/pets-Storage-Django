from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from accounts.forms import CreateNewUserForm, LoginUserForm
from django.urls import reverse_lazy


class CreateUser(CreateView):
    model = User
    form_class = CreateNewUserForm
    template_name = "form_acc.html"
    context_object_name = "form"
    success_url = reverse_lazy("storage:Home")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        if form.cleaned_data["is_superuser"]:
            new_user.is_superuser = True
            new_user.is_staff = True
        new_user.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Novo Usuário"
        context["form_btn_success"] = "Cadastrar Funcionário"
        context["retrieve"] = "storage:Home"
        return context


class LoginUser(LoginView):
    form_class = LoginUserForm
    context_object_name = "form"
    template_name = "form_acc.html"
    success_url = reverse_lazy("storage:Home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Fazer Login"
        context["form_btn_success"] = "Entrar em sua conta"
        context["retrieve"] = "storage:Home"
        return context


class LogoutUser(LogoutView):
    next_page = reverse_lazy("accounts:login")
