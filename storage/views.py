from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, F
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from storage.models import StorageFoods, Brands, StorageMoviments
from storage.forms import NewFood, Newbrand

# Create your views here.


class HomeStorage(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = StorageFoods
    context_object_name = "pet_food"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("brand")
        filter_data = self.request.GET.get("filter")

        if filter_data:
            queryset = queryset.filter(Q(food__icontains=filter_data) | Q(animal__iexact=filter_data))

        return queryset


class AlertHomeStorage(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "alerthome.html"
    model = StorageFoods
    context_object_name = "pet_food"

    def get_queryset(self):
        return StorageFoods.objects.filter(alert_quantity__gt=F('quantity')).order_by("brand")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")


class DetailFood(LoginRequiredMixin, DetailView):
    template_name = "detail.html"
    model = StorageFoods
    context_object_name = "item"


class CreateFood(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = NewFood
    success_url = reverse_lazy("storage:Home")
    template_name = "createfood.html"
    context_object_name = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def form_valid(self, form):
        response = super().form_valid(form)
        return response


class UpdateFood(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = NewFood
    model = StorageFoods
    template_name = "create.html"
    context_object_name = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def get_success_url(self):
        return reverse_lazy("storage:Detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Editar Ração"
        context["form_btn_success"] = "Salvar Alterações"
        context["retrieve"] = "storage:Home"
        return context


class DeleteFood(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = StorageFoods
    success_url = reverse_lazy("storage:Home")

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)


class CreateBrand(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    form_class = Newbrand
    success_url = "../../"
    template_name = "createbrand.html"
    context_object_name = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Adicionar Nova Marca"
        context["form_btn_success"] = "Criar Marca"
        context["retrieve"] = "storage:Home"
        return context


class UpdateBrand(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = Newbrand
    model = Brands
    template_name = "create.html"
    context_object_name = "form"

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return redirect("storage:Home")

    def get_success_url(self):
        return reverse_lazy("storage:Detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Editar Marca"
        context["form_btn_success"] = "Salvar Alterações"
        context["retrieve"] = "storage:Home"
        return context


def CreateTransition(request, pk):
    if request.method == 'POST':
        quantidade = int(request.POST.get('quantidade', 0))
        tipo_movimentacao = request.POST.get('tipo_movimentacao')
        success_url = reverse_lazy('storage:Detail', kwargs={'pk': pk})

        if tipo_movimentacao == 'buy':
            StorageFoods.objects.filter(id=pk).update(quantity=F("quantity") + quantidade)
            StorageMoviments.objects.create(
                user=request.user,
                food=StorageFoods.objects.get(pk=pk),
                quantity=quantidade,
                moviment_type='Compra',
            )

        elif tipo_movimentacao == 'sell':
            StorageFoods.objects.filter(id=pk).update(quantity=F("quantity") - quantidade)
            StorageMoviments.objects.create(
                user=request.user,
                food=StorageFoods.objects.get(pk=pk),
                quantity=quantidade,
                moviment_type='Venda',
            )

        return HttpResponseRedirect(success_url)


class ShowTransitions(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = "transitions.html"
    model = StorageMoviments
    context_object_name = "data"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        queryset = StorageMoviments.objects.order_by("-date")
        filter_data = self.request.GET.get("filter")

        if filter_data:
            queryset = queryset.filter(user__username__icontains=filter_data)

        return queryset
