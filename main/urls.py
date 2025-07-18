from django.urls import path

from . import views

app_name = "main"

urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard_view"),
    path("dash/tomorrow/", views.TomorrowOrdersView.as_view(), name="tomorrow_orders_view"),
    path("dash/subscriptions/", views.SubscriptionListView.as_view(), name="subscription_list"),
    path("dash/subscriptions/detail/<str:pk>/", views.SubscriptionDetailView.as_view(), name="subscription_detail"),
    path("customers/", views.CustomerListView.as_view(), name="customer_list"),
    path("customers/detail/<str:pk>/", views.CustomerDetailView.as_view(), name="customer_detail"),
    path("items/", views.ItemMasterListView.as_view(), name="item_list"),
    path("items/detail/<str:pk>/", views.ItemMasterDetailView.as_view(), name="item_detail"),
    path("orders/", views.MealOrderListView.as_view(), name="mealorder_list"),
    path("orders/detail/<str:pk>/", views.MealOrderDetailView.as_view(), name="mealorder_detail"),
    path("orders/data/", views.MealOrderListData.as_view(), name="mealorder_list_data"),
    path("requests/", views.PreferenceRequestListView.as_view(), name="subscriptionrequest_list"),
    path("requests/detail/<str:pk>/", views.PreferenceRequestDetailView.as_view(), name="subscriptionrequest_detail"),
    path("requests/update/<str:pk>/", views.PreferenceRequestUpdateView.as_view(), name="subscriptionrequest_update"),
    path("requests/approve/<str:pk>/", views.PreferenceApproveView.as_view(), name="subscriptionrequest_approve"),
    path("requests/reject/<str:pk>/", views.PreferenceRejectView.as_view(), name="subscriptionrequest_reject"),
    path("requests/print/<str:pk>/", views.PreferencePrintView.as_view(), name="subscriptionrequest_print"),
    path("help/", views.HelpView.as_view(), name="help_view"),
    path("history/detail/<str:pk>/", views.HistoryDetailView.as_view(), name="history_detail_view"),
    path("donate/<str:pk>/", views.DonateMealOrderView.as_view(), name="donatemealorder_view"),
    path("update_status/<str:pk>/", views.UpdateMealOrderStatusView.as_view(), name="updatemealorderstatus_view"),
    path("change_menu/", views.ChangeMenuView.as_view(), name="changemenu_view"),
    # Pages
    path("history/", views.HistoryView.as_view(), name="history_view"),
    # orders
    path("orders/approve/<str:pk>/", views.approve_preference, name="approve-preference"),
    path("order/detail/<str:pk>/", views.edit_preference, name="edit-preference"),
]
