from django.contrib import admin
from .models import Brands, StorageFoods, StorageMoviments, StorageMonthlyReport

# Register your models here.


class AdminBrands(admin.ModelAdmin):
    list_display = ("id", "name", "corporate", "seller", "contact_seller")
    search_fields = ("name",)
    ordering = ("id",)


class AdminStorage(admin.ModelAdmin):
    list_display = ("id", "brand", "food", "weight", "quantity", "animal", "buy_price", "sell_price_card")
    search_fields = ("food", "animal")
    ordering = ("-quantity",)


class AdminTransition(admin.ModelAdmin):
    list_display = ("id", "user", "food", "moviment_type", "quantity", "date")
    ordering = ("-date",)


class AdminReport(admin.ModelAdmin):
    list_display = ("report_date", "select_food", "starter_quantity", "buy_quantity", "sell_quantity", "ending_quantity")
    ordering = ("-report_date",)


admin.site.register(StorageMoviments, AdminTransition)
admin.site.register(Brands, AdminBrands)
admin.site.register(StorageFoods, AdminStorage)
admin.site.register(StorageMonthlyReport, AdminReport)
