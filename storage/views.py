from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q
from django.shortcuts import get_object_or_404
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
        return reverse_lazy("storage:Detail", kwargs={"pk": self.object.pk})

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



class UpdateBrand(UpdateView):
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

        if quantidade <= 0:
            messages.error(request, "A quantidade deve ser maior que zero.")
            return redirect('storage:Detalhe', pk=pk)

        # Atualiza o estoque e cria o histórico
        if tipo_movimentacao == 'buy':
            food_item.quantity += quantidade
            TransactionHistory.objects.create(
                user=request.user,
                food=food_item,
                quantity=quantidade,
                movement_type='Compra',
            )
            messages.success(request, f"Você comprou {quantidade} unidades de {food_item.food}.")
        elif tipo_movimentacao == 'sell':
            if food_item.quantity >= quantidade:
                food_item.quantity -= quantidade
                TransactionHistory.objects.create(
                    user=request.user,
                    food=food_item,
                    quantity=quantidade,
                    movement_type='Venda',
                )
                messages.success(request, f"Você vendeu {quantidade} unidades de {food_item.food}.")
            else:
                messages.error(request, "Estoque insuficiente para a venda.")
        
        food_item.save()
        return redirect('storage:Detalhe', pk=pk)

    return redirect('storage:Home')