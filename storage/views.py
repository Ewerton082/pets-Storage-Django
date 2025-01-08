from django.views.generic import ListView
from storage.models import StorageFoods

# Create your views here.


class HomeStorage(ListView):
    template_name = "home.html"
    model = StorageFoods
    context_object_name = "pet_food"

    def get_queryset(self):
        queryset = super().get_queryset().order_by("food")
        filter_data = self.request.GET.get("filter")

        if filter_data:
            queryset = queryset.filter(food__icontains=filter_data)

        return queryset
