from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="home_view"),
    path("dash/", views.DashboardView.as_view(), name="dashboard_view"),
    path("dash/tomorrow/", views.TomorrowOrdersView.as_view(), name="tomorrow_orders_view"),
    path("dash/subscriptions/", views.SubscriptionListView.as_view(), name="subscription_list"),
    path("dash/subscriptions/detail/<str:pk>/", views.SubscriptionDetailView.as_view(), name="subscription_detail"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/detail/<str:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("combos/", views.ComboListView.as_view(), name="combo_list"),
    path("combos/detail/<str:pk>/", views.ComboDetailView.as_view(), name="combo_detail"),
    path("orders/", views.MealOrderListView.as_view(), name="mealorder_list"),
    path("orders/detail/<str:pk>/", views.MealOrderDetailView.as_view(), name="mealorder_detail"),
    path("orders/data/", views.MealOrderListData.as_view(), name="mealorder_list_data"),
    path("requests/", views.SubscriptionRequestListView.as_view(), name="subscriptionrequest_list"),
    path("requests/detail/<str:pk>/", views.SubscriptionRequestDetailView.as_view(), name="subscriptionrequest_detail"),
    path("requests/update/<str:pk>/", views.SubscriptionRequestUpdateView.as_view(), name="subscriptionrequest_update"),
    path("requests/approve/<str:pk>/", views.SubscriptionRequestApproveView.as_view(), name="subscriptionrequest_approve"),
    path("requests/reject/<str:pk>/", views.SubscriptionRequestRejectView.as_view(), name="subscriptionrequest_reject"),
    path("requests/print/<str:pk>/", views.SubscriptionRequestPrintView.as_view(), name="subscriptionrequest_print"),
    path("help/", views.HelpView.as_view(), name="help_view"),
    path("history/detail/<str:pk>/", views.HistoryDetailView.as_view(), name="history_detail_view"),
    path("donate/<str:pk>/", views.DonateMealOrderView.as_view(), name="donatemealorder_view"),
    path("update_status/<str:pk>/", views.UpdateMealOrderStatusView.as_view(), name="updatemealorderstatus_view"),
    # Pages
    path("eats/all/", views.AllEatsView.as_view(), name="all_eats_view"),
    path("history/", views.HistoryView.as_view(), name="history_view"),
]
