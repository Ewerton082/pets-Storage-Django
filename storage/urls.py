from django.urls import path
from storage.views import HomeStorage

urlpatterns = [
    path("", HomeStorage.as_view())
]