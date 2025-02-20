from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import redirect
from accounts.forms import CreateNewUserForm, LoginUserForm


class CreateUser(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = CreateNewUserForm
    template_name = "register_template.html"
    context_object_name = "form"
    success_url = reverse_lazy("storage:Home")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        if form.cleaned_data["is_superuser"]:
            new_user.is_superuser = True
            new_user.is_staff = True
        new_user.save()
        return super().form_valid(form)



class LoginUser(LoginView):
    form_class = LoginUserForm
    context_object_name = "form"
    template_name = "login_template.html"
    success_url = reverse_lazy("storage:Home")

    def get_success_url(self):
        return self.success_url



class LogoutUser(LoginRequiredMixin, LogoutView):
    next_page = reverse_lazy("accounts:Login")
