from django.urls import path
from accounts.views import CreateUser

urlpatterns = [
    path("register/", CreateUser.as_view(), name="Register")
]