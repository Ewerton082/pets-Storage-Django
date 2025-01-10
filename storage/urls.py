from django.urls import path
from storage.views import HomeStorage, CreateFood

urlpatterns = [
    path("", HomeStorage.as_view()),
    path("create/", CreateFood.as_view()),
]