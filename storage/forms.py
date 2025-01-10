from django.forms import ModelForm, TextInput, Select, NumberInput, FileInput
from storage.models import StorageFoods


class NewFood(ModelForm):
    class Meta:
        model = StorageFoods
        fields = fields = ["brand", "food", "weight", "quantity", "animal", "buy_price",
                            "sell_price_card", "sell_price_money", "image"]
        exclude = ["id",]
        widgets = {
            "brand": Select(attrs={"class": "form-select"}),
            "food" : TextInput(attrs={"class": "form-control"}),
            "weight": Select(attrs={"class": "form-select"}),
            "quantity": NumberInput(attrs={"class": "form-control"}),
            "animal": Select(attrs={"class": "form-select"}),
            "buy_price": NumberInput(attrs={"class": "form-control"}),
            "sell_price_card": NumberInput(attrs={"class": "form-control"}),
            "sell_price_money": NumberInput(attrs={"class": "form-control"}),
            "image": FileInput(attrs={"class": "form-control"}),

        }