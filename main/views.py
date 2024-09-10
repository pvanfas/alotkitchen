from collections import defaultdict
from datetime import datetime

from django.db.models import Sum
from django.shortcuts import redirect
from django.utils import timezone

from main.mixins import HybridDetailView, HybridListView, HybridUpdateView
from users.models import CustomUser as User
from users.tables import UserTable

from .mixins import HybridTemplateView
from .models import Combo, MealOrder, Subscription, SubscriptionRequest
from .tables import ComboTable, MealOrderDataTable, MealOrderTable, StandardMealOrderTable, SubscriptionRequestTable, SubscriptionTable

# permissions = ("Administrator", "KitchenManager", "Delivery", "Customer", "Accountant")


def get_week_of_month():
    today = timezone.localdate()
    day_of_month = today.day
    week_number = (day_of_month - 1) // 7 + 1
    return week_number


def get_day_name():
    today = timezone.localdate()
    day_name = today.strftime("%A")
    return day_name


def get_week_value(n):
    return 2 if n % 2 == 0 else 1


class DashboardView(HybridListView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer", "Accountant")
    model = MealOrder
    context_object_name = "orders"

    def get_table_class(self):
        if self.request.user.usertype == "KitchenManager":
            return StandardMealOrderTable
        return MealOrderTable

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return MealOrder.objects.filter(date=datetime.today(), user=self.request.user, is_active=True)
        else:
            return MealOrder.objects.filter(date=datetime.today(), is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset().values("combo__mealtype", "combo__name").annotate(total_quantity=Sum("quantity"))
        data = defaultdict(list)
        for entry in qs:
            mealtype = entry["combo__mealtype"]
            combo_name = entry["combo__name"]
            total_quantity = entry["total_quantity"]
            data[mealtype].append((combo_name, total_quantity))
        context["datas"] = dict(data)
        return context


class TomorrowOrdersView(HybridListView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer", "Accountant")
    model = MealOrder
    table_class = MealOrderTable
    context_object_name = "orders"
    title = "Tomorrow's Orders"

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), user=self.request.user, is_active=True)
        else:
            return MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        qs = self.get_queryset().values("combo__mealtype", "combo__name").annotate(total_quantity=Sum("quantity"))
        data = defaultdict(list)
        for entry in qs:
            mealtype = entry["combo__mealtype"]
            combo_name = entry["combo__name"]
            total_quantity = entry["total_quantity"]
            data[mealtype].append((combo_name, total_quantity))
        context["datas"] = dict(data)
        return context


class MealOrderListView(HybridListView):
    permissions = ("Administrator", "Accountant")
    model = MealOrder
    title = "Order Master"
    table_class = MealOrderTable
    filterset_fields = ("user", "combo", "subscription_plan", "date", "status")

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class MealOrderDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Administrator", "Accountant")


class MealOrderListData(HybridListView):
    model = MealOrder
    permissions = ("Administrator", "Accountant")
    title = "Order Master Excel"
    table_class = MealOrderDataTable
    template_name = "app/main/mealorder_list_data.html"

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class ComboListView(HybridListView):
    filterset_fields = ("mealtype", "is_veg")
    search_fields = ("name",)
    permissions = ("Administrator", "Accountant", "KitchenManager")
    model = Combo
    title = "Item Master"
    table_class = ComboTable


class ComboDetailView(HybridDetailView):
    model = Combo
    permissions = ("Administrator", "Accountant", "KitchenManager")


class CustomerListView(HybridListView):
    filterset_fields = ("username", "email")
    search_fields = ("username", "email", "mobile")
    permissions = ("Administrator",)
    model = User
    title = "Customers"
    table_class = UserTable

    def get_queryset(self):
        return User.objects.filter(usertype="Customer", is_active=True)


class CustomerDetailView(HybridDetailView):
    model = User
    permissions = ("Administrator",)


class SubscriptionRequestListView(HybridListView):
    metadata = {"expand": "newpage"}
    model = SubscriptionRequest
    permissions = ("Administrator",)
    title = "Subscription Requests"
    table_class = SubscriptionRequestTable
    filterset_fields = ("user", "plan", "start_date", "status")


class SubscriptionRequestDetailView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator",)
    template_name = "app/main/request_detail.html"


class SubscriptionRequestUpdateView(HybridUpdateView):
    model = SubscriptionRequest
    permissions = ("Administrator",)
    exclude = ("status", "is_active", "user")


class SubscriptionRequestApproveView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator",)

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        subscription, _ = Subscription.objects.get_or_create(
            request=data,
            user=data.user,
            plan=data.plan,
            start_date=data.start_date,
            end_date=data.start_date + timezone.timedelta(days=data.plan.validity),
        )
        data.status = "APPROVED"
        data.save()
        return redirect("main:subscription_detail", pk=subscription.pk)


class SubscriptionRequestRejectView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator",)

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        data.status = "REJECTED"
        data.save()
        return redirect("main:subscriptionrequest_detail", pk=data.pk)


class SubscriptionRequestPrintView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator",)
    template_name = "app/main/request_print.html"


class SubscriptionListView(HybridListView):
    model = Subscription
    filterset_fields = ("user", "plan", "start_date", "end_date")
    search_fields = ("user",)
    permissions = ("Administrator", "Customer")
    table_class = SubscriptionTable


class SubscriptionDetailView(HybridDetailView):
    model = Subscription
    permissions = ("Administrator", "Customer")


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


# class FeaturedEatsView(HybridTemplateView):
#     template_name = "app/main/featured_eats.html"
#     permissions = ("Customer", "KitchenManager")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context["week_number"] = get_week_of_month()
#         context["day_name"] = get_day_name()
#         available_combos = Combo.objects.filter(
#             is_active=True,
#             available_weeks=get_week_value(get_week_of_month()),
#             available_days=get_day_name(),
#         )
#         context["breakfasts"] = available_combos.filter(is_active=True, mealtype="BREAKFAST")
#         context["lunches"] = available_combos.filter(is_active=True, mealtype="LUNCH")
#         context["dinners"] = available_combos.filter(is_active=True, mealtype="DINNER")
#         return context


# class AllEatsView(ListView):
#     template_name = "app/main/all_eats.html"
#     model = ItemCategory
#     context_object_name = "categories"
#     permissions = ("Administrator", "Customer", "KitchenManager")


# class HistoryView(HybridListView):
#     template_name = "app/main/history.html"
#     model = MealOrder
#     filterset_fields = ()
#     table_class = MealOrderTable
#     search_fields = ("combo__name",)
#     permissions = ("Customer",)

#     def get_queryset(self):
#         return MealOrder.objects.filter(user=self.request.user, is_active=True)


# class HistoryDetailView(HybridDetailView):
#     model = MealOrder
#     permissions = ("Customer",)


# class PricingView(HybridTemplateView):
#     template_name = "app/main/pricing.html"
#     permissions = ("Administrator", "Customer")

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         weekly_plans = SubscriptionPlan.objects.filter(is_active=True)
#         monthly_plans = SubscriptionPlan.objects.filter(is_active=True)
#         context["weekly_plans"] = weekly_plans
#         context["monthly_plans"] = monthly_plans
#         return context
