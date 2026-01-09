from django.urls import path
from .views import chatbot, register, user_login

urlpatterns = [
    path("", chatbot, name="chatbot"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
]