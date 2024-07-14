from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("dash/", views.DashboardView.as_view(), name="dashboard_view"),
    # SubscriptionPlan
    path("dash/subscriptionplans/", views.SubscriptionPlanListView.as_view(), name="subscriptionplan_list"),
    path("dash/subscriptionplans/create/", views.SubscriptionPlanCreateView.as_view(), name="subscriptionplan_create"),
    path("dash/subscriptionplans/detail/<str:pk>/", views.SubscriptionPlanDetailView.as_view(), name="subscriptionplan_detail"),
    path("dash/subscriptionplans/update/<str:pk>/", views.SubscriptionPlanUpdateView.as_view(), name="subscriptionplan_update"),
    path("dash/subscriptionplans/delete/<str:pk>/", views.SubscriptionPlanDeleteView.as_view(), name="subscriptionplan_delete"),
    # Branch
    path("dash/branches/", views.BranchListView.as_view(), name="branch_list"),
    path("dash/branches/create/", views.BranchCreateView.as_view(), name="branch_create"),
    path("dash/branches/detail/<str:pk>/", views.BranchDetailView.as_view(), name="branch_detail"),
    path("dash/branches/update/<str:pk>/", views.BranchUpdateView.as_view(), name="branch_update"),
    path("dash/branches/delete/<str:pk>/", views.BranchDeleteView.as_view(), name="branch_delete"),
    # Pages
    path("favourites/", views.FavouritesView.as_view(), name="favourites_view"),
    path("featured_eats/", views.FeaturedEatsView.as_view(), name="featured_eats_view"),
    path("wallet/", views.WalletView.as_view(), name="wallet_view"),
    path("pricing/", views.PricingView.as_view(), name="pricing_view"),
    path("manage_account/", views.ManageAccountView.as_view(), name="manage_account_view"),
    path("help/", views.HelpView.as_view(), name="help_view"),

]
