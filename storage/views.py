from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from storage.models import StorageFoods, Brands, StorageMoviments
from storage.forms import NewFood, Newbrand
from core.validation import superuser_required

# Create your views here.



class HomeStorage(LoginRequiredMixin, ListView):
    template_name = "home.html"
    model = StorageFoods
    context_object_name = "pet_food"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("food")
        filter_data = self.request.GET.get("filter")

        if filter_data:
            queryset = queryset.filter(Q(food__icontains=filter_data) | Q(animal__iexact=filter_data))

        return queryset



class DetailFood(LoginRequiredMixin, DetailView):
    template_name = "detail.html"
    model = StorageFoods
    context_object_name = "item"




class CreateFood(LoginRequiredMixin, CreateView):
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



class UpdateFood(LoginRequiredMixin, UpdateView):
    form_class = NewFood
    model = StorageFoods
    template_name = "create.html"
    context_object_name = "form"

    def get_success_url(self):
        return reverse_lazy("storage:Detail", kwargs={"pk": self.object.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_title"] = "Editar Ração"
        context["form_btn_success"] = "Salvar Alterações"
        context["retrieve"] = "storage:Home"
        return context



class DeleteFood(LoginRequiredMixin, DeleteView):
    model = StorageFoods
    success_url = reverse_lazy("storage:Home")

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return HttpResponseRedirect(self.success_url)



class CreateBrand(LoginRequiredMixin, CreateView):
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




class UpdateBrand(LoginRequiredMixin, UpdateView):
    form_class = Newbrand
    model = Brands
    template_name = "create.html"
    context_object_name = "form"

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
        food_item = get_object_or_404(StorageFoods, pk=pk)
        quantidade = int(request.POST.get('quantidade', 0))
        tipo_movimentacao = request.POST.get('tipo_movimentacao')
        print(tipo_movimentacao)
        success_url = reverse_lazy('storage:Detail', kwargs={'pk': food_item.pk} )

        if tipo_movimentacao == 'buy':
            food_item.quantity += quantidade
            StorageMoviments.objects.create(
                user=request.user,
                food=food_item,
                quantity=quantidade,
                moviment_type='Compra',
            )

        elif tipo_movimentacao == 'sell':
            if food_item.quantity >= quantidade:
                food_item.quantity -= quantidade
                print(food_item.quantity)
                StorageMoviments.objects.create(
                    user=request.user,
                    food=food_item,
                    quantity=quantidade,
                    moviment_type='Venda',
                )

        food_item.save()
        return HttpResponseRedirect(success_url)
    