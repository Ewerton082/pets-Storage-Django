from django.urls import path
from accounts.views import CreateUser, LoginUser, LogoutUser

app_name = "accounts"

urlpatterns = [
    path("register/", CreateUser.as_view(), name="Register"),
    path("login/", LoginUser.as_view(), name="Login"),
    path("logout/", LogoutUser.as_view(), name="Logout"),
]
