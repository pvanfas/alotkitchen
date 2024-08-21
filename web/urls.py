from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<slug:slug>/", views.page_view, name="page_view"),
]
