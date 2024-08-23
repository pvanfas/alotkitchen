from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<slug:slug>/", views.page_view, name="page_view"),
    path("Essential/", views.essential, name="essential"),
    path("ClassicVeg/", views.classicveg, name="classicveg"),
    path("ClassicNonVeg/", views.classicnonveg, name="classicnonveg"),
    path("StandardNonVeg/", views.standardnonveg, name="standardnonveg"),
    path("StandardVeg/", views.standardveg, name="standardveg"),
    path("Premium/", views.premium, name="premium"),
    path("Signature/", views.signature, name="signature"),
]
