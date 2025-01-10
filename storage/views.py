from django.views.generic import ListView, CreateView
from django.db.models import Q
from storage.models import StorageFoods
from storage.forms import NewFood

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


class CreateFood(CreateView):
    form_class = NewFood
    success_url = "../"
    template_name = "create.html"
    context_object_name = "form"
