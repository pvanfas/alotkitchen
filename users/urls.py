from django.urls import path

from .views import custom_register

app_name = "users"

urlpatterns = [
    path("register/", custom_register, name="custom_register"),
]
