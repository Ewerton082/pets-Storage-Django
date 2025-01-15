from django.views.generic import CreateView
from django.contrib.auth.models import User
from accounts.forms import CreateNewUserForm
from django.urls import reverse_lazy


class CreateUser(CreateView):
    model = User
    form_class = CreateNewUserForm
    template_name = "create.html"
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
