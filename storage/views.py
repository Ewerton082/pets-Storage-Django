from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from storage.models import StorageFoods, Brands
from storage.forms import NewFood, Newbrand

# Create your views here.


class HomeStorage(ListView):
    template_name = "home.html"
    model = StorageFoods
    context_object_name = "pet_food"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("food")
        filter_data = self.request.GET.get("filter")

        if filter_data:
            queryset = queryset.filter(Q(food__icontains=filter_data) | Q(animal__iexact=filter_data))

        return queryset


class DetailFood(DetailView):
    template_name = "detail.html"
    model = StorageFoods
    context_object_name = "item"


class CreateFood(CreateView):
    form_class = NewFood
    success_url = reverse_lazy("storage:Home")
    template_name = "create.html"
    context_object_name = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Adicionar Nova Ração"
        context["form_btn_success"] = "Criar Ração"
        context["retrieve"] = "storage:Home"
        return context


class UpdateFood(UpdateView):
    form_class = NewFood
    model = StorageFoods
    template_name = "create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse_lazy("Detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Editar Ração"
        context["form_btn_success"] = "Salvar Alterações"
        context["retrieve"] = "storage:Home"
        return context


class DeleteFood(DeleteView):
    model = StorageFoods
    success_url = reverse_lazy("storage:Home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class CreateBrand(CreateView):
    form_class = Newbrand
    success_url = "../../"
    template_name = "create.html"
    context_object_name = "form"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Adicionar Nova Marca"
        context["form_btn_success"] = "Criar Marca"
        context["retrieve"] = "storage:Home"
        return context


class CreateTransition(CreateView):
    pass