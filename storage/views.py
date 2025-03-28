from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.db.models import Q, F, Sum
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from storage.models import StorageFoods, Brands, StorageMoviments, StorageMonthlyReport
from django.contrib.auth.models import User
from storage.forms import NewFood, Newbrand
from django.utils import timezone
from datetime import timedelta

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["sellers"] = User.objects.all()
        context["selected_seller"] = User.objects.get(pk=self.request.user.pk)

        return context


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
    template_name = "createfood.html"
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
    template_name = "createbrand.html"
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
        seller = request.POST.get("seller")
        seller = User.objects.get(pk=seller)
        tipo_movimentacao = request.POST.get('tipo_movimentacao')
        success_url = reverse_lazy('storage:Home')
        product = StorageFoods.objects.get(pk=pk)

        if tipo_movimentacao == 'buy':
            StorageFoods.objects.filter(id=pk).update(quantity=F("quantity") + quantidade)
            StorageMoviments.objects.create(
                user=seller,
                food=StorageFoods.objects.get(pk=pk),
                quantity=quantidade,
                moviment_type='Compra',
            )

            today = timezone.now().date()
            last_monday = today - timezone.timedelta(days=today.weekday())
            report, _ = StorageMonthlyReport.objects.get_or_create(
                report_date=last_monday,
                select_food=product,
                defaults={
                    "starter_quantity": product.quantity,
                    "ending_quantity": product.quantity
                }
            )
            report.buy_quantity += quantidade
            report.ending_quantity += quantidade
            report.date = last_monday
            report.save()

        elif tipo_movimentacao == 'sell':
            StorageFoods.objects.filter(id=pk).update(quantity=F("quantity") - quantidade)
            StorageMoviments.objects.create(
                user=seller,
                food=StorageFoods.objects.get(pk=pk),
                quantity=quantidade,
                moviment_type='Venda',
            )

            today = timezone.now().date()
            last_monday = today - timezone.timedelta(days=today.weekday())
            report, _ = StorageMonthlyReport.objects.get_or_create(
                report_date=last_monday,
                select_food=product,
                defaults={
                    "starter_quantity": product.quantity,
                    "ending_quantity": product.quantity
                }
            )
            report.sell_quantity += quantidade
            report.ending_quantity -= quantidade
            report.date = last_monday
            report.save()

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


class ShowRelatory(LoginRequiredMixin, UserPassesTestMixin, ListView):
    context_object_name = "report"
    model = StorageMonthlyReport
    template_name = "weekreport.html"

    def test_func(self):
        return self.request.user.is_superuser

    def get_queryset(self):
        selected_date = self.request.GET.get("report_date")
        if selected_date:
            queryset = StorageMonthlyReport.objects.filter(report_date=selected_date).order_by("select_food")
        else:
            today = timezone.now().date()
            start_week = today - timedelta(days=today.weekday())
            queryset = StorageMonthlyReport.objects.filter(report_date=start_week).order_by("select_food")

        return queryset

    def get_context_data(self, **kwargs):
        today = timezone.now().date()
        start_week = today - timedelta(days=today.weekday())

        available_dates = StorageMonthlyReport.objects.values_list("report_date", flat=True).distinct().order_by("-report_date")
        selected_date = self.request.GET.get("report_date")
        filter_date = selected_date if selected_date else start_week

        context = super().get_context_data(**kwargs)

        top_sales = (StorageMonthlyReport.objects.filter(report_date=filter_date).values("select_food__food").annotate(all_sales=Sum("sell_quantity")).order_by("-all_sales")[:5])
        top_buys = (StorageMonthlyReport.objects.filter(report_date=filter_date).values("select_food__food").annotate(all_buys=Sum("buy_quantity")).order_by("-all_buys")[:5])

        context["available_dates"] = available_dates
        context["selected_date"] = filter_date
        context["top_sales"] = top_sales
        context["top_buys"] = top_buys
        return context
