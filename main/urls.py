from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard_view"),
    # SubscriptionPlan
    path("subscriptionplans/", views.SubscriptionPlanListView.as_view(), name="subscriptionplan_list"),
    path("subscriptionplans/create/", views.SubscriptionPlanCreateView.as_view(), name="subscriptionplan_create"),
    path("subscriptionplans/detail/<str:pk>/", views.SubscriptionPlanDetailView.as_view(), name="subscriptionplan_detail"),
    path("subscriptionplans/update/<str:pk>/", views.SubscriptionPlanUpdateView.as_view(), name="subscriptionplan_update"),
    path("subscriptionplans/delete/<str:pk>/", views.SubscriptionPlanDeleteView.as_view(), name="subscriptionplan_delete"),
    # Branch
    path("branches/", views.BranchListView.as_view(), name="branch_list"),
    path("branches/create/", views.BranchCreateView.as_view(), name="branch_create"),
    path("branches/detail/<str:pk>/", views.BranchDetailView.as_view(), name="branch_detail"),
    path("branches/update/<str:pk>/", views.BranchUpdateView.as_view(), name="branch_update"),
    path("branches/delete/<str:pk>/", views.BranchDeleteView.as_view(), name="branch_delete"),
]
