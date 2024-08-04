from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="home_view"),
    path("dash/", views.DashboardView.as_view(), name="dashboard_view"),
    path("dash/tomorrow/", views.TomorrowOrdersView.as_view(), name="tomorrow_orders_view"),
    # SubscriptionPlan
    # path("dash/subscriptionplans/", views.SubscriptionPlanListView.as_view(), name="subscriptionplan_list"),
    # path("dash/subscriptionplans/create/", views.SubscriptionPlanCreateView.as_view(), name="subscriptionplan_create"),
    path("dash/subscriptionplans/detail/<str:pk>/", views.SubscriptionPlanDetailView.as_view(), name="subscriptionplan_detail"),
    # path("dash/subscriptionplans/update/<str:pk>/", views.SubscriptionPlanUpdateView.as_view(), name="subscriptionplan_update"),
    # path("dash/subscriptionplans/delete/<str:pk>/", views.SubscriptionPlanDeleteView.as_view(), name="subscriptionplan_delete"),
    # Subscription
    path("dash/subscriptions/", views.SubscriptionListView.as_view(), name="subscription_list"),
    path("dash/subscriptions/detail/<str:pk>/", views.SubscriptionDetailView.as_view(), name="subscription_detail"),
    # Branch
    path("dash/branches/", views.BranchListView.as_view(), name="branch_list"),
    # path("dash/branches/create/", views.BranchCreateView.as_view(), name="branch_create"),
    # path("dash/branches/detail/<str:pk>/", views.BranchDetailView.as_view(), name="branch_detail"),
    # path("dash/branches/update/<str:pk>/", views.BranchUpdateView.as_view(), name="branch_update"),
    # path("dash/branches/delete/<str:pk>/", views.BranchDeleteView.as_view(), name="branch_delete"),
    # Address
    path("manage_address/", views.UserAddressListView.as_view(), name="useraddress_list"),
    path("manage_address/create/", views.UserAddressCreateView.as_view(), name="useraddress_create"),
    path("manage_address/update/<str:pk>/", views.UserAddressUpdateView.as_view(), name="useraddress_update"),
    path("manage_address/delete/<str:pk>/", views.UserAddressDeleteView.as_view(), name="useraddress_delete"),
    # Pages
    # path("favourites/", views.FavouritesView.as_view(), name="favourites_view"),
    path("featured_eats/", views.FeaturedEatsView.as_view(), name="featured_eats_view"),
    path("eats/all/", views.AllEatsView.as_view(), name="all_eats_view"),
    path("eats/view/<str:pk>/", views.CategoryDetailView.as_view(), name="category_detail_view"),
    path("history/", views.HistoryView.as_view(), name="history_view"),
    path("history/detail/<str:pk>/", views.HistoryDetailView.as_view(), name="history_detail_view"),
    path("pricing/", views.PricingView.as_view(), name="pricing_view"),
    path("help/", views.HelpView.as_view(), name="help_view"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
]
