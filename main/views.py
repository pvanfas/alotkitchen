from collections import defaultdict
from datetime import datetime

from django.db.models import Sum
from django.shortcuts import redirect
from django.urls import reverse
from django.utils import timezone
from django.views.generic import ListView

from main.mixins import HybridDetailView, HybridListView, HybridUpdateView
from users.models import CustomUser as User
from users.tables import UserTable

from .forms import SubscriptionAddressForm
from .mixins import HybridTemplateView
from .models import Combo, ItemCategory, MealOrder, Subscription, SubscriptionRequest
from .tables import ComboTable, MealOrderDataTable, MealOrderTable, StandardMealOrderTable, StandardSubscriptionTable, SubscriptionRequestTable, SubscriptionTable

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
        elif self.request.user.usertype == "Delivery":
            return StandardMealOrderTable
        return MealOrderTable

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return MealOrder.objects.filter(date=datetime.today(), user=self.request.user, is_active=True)
        elif self.request.user.usertype == "Delivery":
            return MealOrder.objects.filter(date=datetime.today(), is_active=True)
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
    permissions = ("Administrator", "Customer")
    exclude = ("status", "is_active", "user")

    def get_form_class(self):
        if self.request.user.usertype == "Customer":
            return SubscriptionAddressForm
        return super().get_form_class()

    def get_template_names(self):
        if self.request.user.usertype == "Customer":
            return "web/select_address.html"
        return super().get_template_names()

    def get_success_url(self):
        if self.request.user.usertype == "Customer":
            return reverse("main:subscription_list")
        return reverse("main:subscriptionrequest_list")


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

    def get_queryset(self):
        if self.request.user.usertype == "Customer":
            return Subscription.objects.filter(user=self.request.user)
        return Subscription.objects.filter(is_active=True)

    def get_table_class(self):
        if self.request.user.usertype == "Customer":
            return StandardSubscriptionTable
        return SubscriptionTable


class SubscriptionDetailView(HybridDetailView):
    model = Subscription
    permissions = ("Administrator", "Customer")


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HistoryDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Customer",)


class AllEatsView(ListView):
    template_name = "app/main/all_eats.html"
    model = ItemCategory
    context_object_name = "categories"
    permissions = ("Administrator", "Customer", "KitchenManager")


class HistoryView(HybridListView):
    template_name = "app/main/history.html"
    model = MealOrder
    filterset_fields = ()
    table_class = MealOrderTable
    search_fields = ("combo__name",)
    permissions = ("Customer",)

    def get_queryset(self):
        return MealOrder.objects.filter(user=self.request.user, is_active=True, date__lt=datetime.today())
