from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.index, name="index"),
    path("page/<slug:slug>/", views.page_view, name="page_view"),
    path("plan/<str:slug>/", views.select_plan, name="select_plan"),
    path("meals/<str:pk>/", views.select_meals, name="select_meals"),
    path("customize/<str:pk>/", views.customize_meals, name="customize_meals"),
    # API Endpoints
    path("api/tier/<str:pk>/", views.SubscriptionPlanListView.as_view(), name="getplans_api"),
    path("api/meals/<str:pk>/", views.SubscriptionPlanMealPlanListView.as_view(), name="getmeals_api"),
    # not verified
    path("tier/<str:pk>/customize/", views.customize_menu, name="customize_menu"),
    path("create_profile/", views.create_profile, name="create_profile"),
    path("select/plan/<str:pk>/", views.select_planx, name="select_planx"),
    path("select/address/<str:pk>/", views.select_address, name="select_address"),
    path("confirm/subscription/<str:pk>/", views.confirm_subscription, name="confirm_subscription"),
    path("complete/subscription/<str:pk>/", views.complete_subscription, name="complete_subscription"),
    # path("test/", views.test, name="test"),
]
