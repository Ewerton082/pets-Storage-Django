from django.urls import path
from storage.views import HomeStorage, CreateFood, DetailFood, CreateBrand, UpdateFood, DeleteFood, CreateTransition, AlertHomeStorage

app_name = "storage"

urlpatterns = [
    path("", HomeStorage.as_view(), name="Home"),
    path("alert/", AlertHomeStorage.as_view(), name="AlertHome"),
    path("create/food/", CreateFood.as_view(), name="Create"),
    path("create/brand/", CreateBrand.as_view(), name="CreateBrand"),
    path("detail/<int:pk>/", DetailFood.as_view(), name="Detail"),
    path("detail/<int:pk>/update/", UpdateFood.as_view(), name="Update"),
    path("detail/<int:pk>/delete/", DeleteFood.as_view(), name="Delete"),
    path("detail/<int:pk>/transition/", CreateTransition, name="Transition"),
    path("transitions/", )
]
