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
    path("create_profile/", views.create_profile, name="create_profile"),
    path("customize_menu/", views.customize_menu, name="customize_menu"),
    path("select/plan/<str:pk>/", views.select_plan, name="select_plan"),
    path("select/address/<str:pk>/", views.select_address, name="select_address"),
    path("confirm/subscription/<str:pk>/", views.confirm_subscription, name="confirm_subscription"),
    path("complete/subscription/<str:pk>/", views.complete_subscription, name="complete_subscription"),
    path("get_plans/", views.get_plans, name="get_plans"),
    path("test/", views.test, name="test"),
]
