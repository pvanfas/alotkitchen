from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="home_view"),
    path("dash/", views.DashboardView.as_view(), name="dashboard_view"),
    path("dash/tomorrow/", views.TomorrowOrdersView.as_view(), name="tomorrow_orders_view"),
    # SubscriptionPlan
    path("dash/subscriptionplans/detail/<str:pk>/", views.SubscriptionPlanDetailView.as_view(), name="subscriptionplan_detail"),
    # Subscription
    path("dash/subscriptions/", views.SubscriptionListView.as_view(), name="subscription_list"),
    path("dash/subscriptions/detail/<str:pk>/", views.SubscriptionDetailView.as_view(), name="subscription_detail"),
    # Branch
    path("dash/branches/", views.BranchListView.as_view(), name="branch_list"),
    # Pages
    path("featured_eats/", views.FeaturedEatsView.as_view(), name="featured_eats_view"),
    path("eats/all/", views.AllEatsView.as_view(), name="all_eats_view"),
    path("eats/view/<str:pk>/", views.CategoryDetailView.as_view(), name="category_detail_view"),
    path("history/", views.HistoryView.as_view(), name="history_view"),
    path("history/detail/<str:pk>/", views.HistoryDetailView.as_view(), name="history_detail_view"),
    path("pricing/", views.PricingView.as_view(), name="pricing_view"),
    path("help/", views.HelpView.as_view(), name="help_view"),
    # Administrator
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/detail/<str:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("combos/", views.ComboListView.as_view(), name="combo_list"),
    path("combos/detail/<str:pk>/", views.ComboDetailView.as_view(), name="combo_detail"),
    path("orders/", views.MealOrderListView.as_view(), name="mealorder_list"),
    path("orders/detail/<str:pk>/", views.MealOrderDetailView.as_view(), name="mealorder_detail"),
    path("orders/data/", views.MealOrderListData.as_view(), name="mealorder_list_data"),
]
