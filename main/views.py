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

from .forms import SubscriptionAddressForm, SubscriptionRequestApprovalForm
from .mixins import HybridTemplateView, HybridView
from .models import Combo, ItemCategory, MealOrder, Subscription, SubscriptionRequest
from .tables import (
    ComboTable,
    CustomerMealOrderTable,
    DeliveryMealOrderTable,
    MealOrderDataTable,
    MealOrderTable,
    StandardMealOrderTable,
    StandardSubscriptionTable,
    SubscriptionRequestTable,
    SubscriptionTable,
)

# permissions = ("Administrator","Manager", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")


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
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")
    model = MealOrder
    context_object_name = "orders"

    def get_table_class(self):
        if self.request.user.usertype == "KitchenManager":
            return StandardMealOrderTable
        elif self.request.user.usertype == "Delivery":
            return DeliveryMealOrderTable
        elif self.request.user.usertype == "Customer":
            return CustomerMealOrderTable
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
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer", "Accountant")
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
    permissions = ("Administrator", "Manager", "Accountant")
    model = MealOrder
    title = "Order Master"
    table_class = MealOrderTable
    filterset_fields = ("user", "combo", "subscription_plan", "date", "status")

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class MealOrderDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Administrator", "Manager", "Accountant")


class MealOrderListData(HybridListView):
    model = MealOrder
    permissions = ("Administrator", "Manager", "Accountant")
    title = "Order Master Excel"
    table_class = MealOrderDataTable
    template_name = "app/main/mealorder_list_data.html"

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class ComboListView(HybridListView):
    filterset_fields = ("mealtype", "is_veg")
    search_fields = ("name",)
    permissions = ("Administrator", "Manager", "Accountant", "KitchenManager")
    model = Combo
    title = "Item Master"
    table_class = ComboTable


class ComboDetailView(HybridDetailView):
    model = Combo
    permissions = ("Administrator", "Manager", "Accountant", "KitchenManager")


class CustomerListView(HybridListView):
    filterset_fields = ("username", "email")
    search_fields = ("username", "email", "mobile")
    permissions = (
        "Administrator",
        "Manager",
    )
    model = User
    title = "Customers"
    table_class = UserTable

    def get_queryset(self):
        return User.objects.filter(usertype="Customer", is_active=True)


class CustomerDetailView(HybridDetailView):
    model = User
    permissions = (
        "Administrator",
        "Manager",
    )


class SubscriptionRequestListView(HybridListView):
    metadata = {"expand": "newpage"}
    model = SubscriptionRequest
    permissions = (
        "Administrator",
        "Manager",
    )
    title = "Subscription Requests"
    table_class = SubscriptionRequestTable
    filterset_fields = ("user", "plan", "start_date", "status")
    template_name = "app/main/subscriptionrequest_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["all_requests_count"] = SubscriptionRequest.objects.filter(is_active=True).count()
        context["pending_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="PENDING").count()
        context["approved_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="APPROVED").count()
        context["rejected_requests_count"] = SubscriptionRequest.objects.filter(is_active=True, status="REJECTED").count()
        return context


class SubscriptionRequestDetailView(HybridDetailView):
    model = SubscriptionRequest
    permissions = (
        "Administrator",
        "Manager",
    )
    template_name = "app/main/request_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubscriptionRequestApprovalForm(self.request.POST or None, instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        instance = self.get_object()
        form = SubscriptionRequestApprovalForm(request.POST, instance=instance)
        subscription, _ = Subscription.objects.get_or_create(
            request=instance,
            user=instance.user,
            plan=instance.plan,
            start_date=instance.start_date,
            end_date=instance.start_date + timezone.timedelta(days=instance.plan.validity),
        )
        instance.status = "APPROVED"
        instance.save()
        if form.is_valid():
            form.save()
            return redirect("main:subscriptionrequest_list")
        return self.get(request, *args, **kwargs)


class SubscriptionRequestUpdateView(HybridUpdateView):
    model = SubscriptionRequest
    permissions = ("Administrator", "Manager", "Customer")
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
    permissions = (
        "Administrator",
        "Manager",
    )

    # def get(self, request, *args, **kwargs):
    #     data = self.get_object()
    #     subscription, _ = Subscription.objects.get_or_create(
    #         request=data,
    #         user=data.user,
    #         plan=data.plan,
    #         start_date=data.start_date,
    #         end_date=data.start_date + timezone.timedelta(days=data.plan.validity),
    #     )
    #     data.status = "APPROVED"
    #     data.save()
    #     return redirect("main:subscription_detail", pk=subscription.pk)


class SubscriptionRequestRejectView(HybridDetailView):
    model = SubscriptionRequest
    permissions = (
        "Administrator",
        "Manager",
    )

    def get(self, request, *args, **kwargs):
        data = self.get_object()
        data.status = "REJECTED"
        data.save()
        return redirect("main:subscriptionrequest_detail", pk=data.pk)


class SubscriptionRequestPrintView(HybridDetailView):
    model = SubscriptionRequest
    permissions = (
        "Administrator",
        "Manager",
    )
    template_name = "app/main/request_print.html"


class SubscriptionListView(HybridListView):
    model = Subscription
    filterset_fields = (
        "user",
        "plan",
        "start_date",
        "end_date",
    )
    search_fields = ("user",)
    permissions = ("Administrator", "Manager", "Customer")
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
    permissions = ("Administrator", "Manager", "Customer")


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
    permissions = ("Administrator", "Manager", "KitchenManager", "Delivery", "Customer")

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
    permissions = ("Administrator", "Manager", "Customer", "KitchenManager")


class HistoryView(HybridListView):
    template_name = "app/main/history.html"
    model = MealOrder
    filterset_fields = ()
    table_class = MealOrderTable
    search_fields = ("combo__name",)
    permissions = ("Customer",)

    def get_queryset(self):
        return MealOrder.objects.filter(user=self.request.user, is_active=True, date__lt=datetime.today())


class DonateMealOrderView(HybridView):
    model = MealOrder
    permissions = ("Customer",)

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def get(self, request, *args, **kwargs):
        order = self.get_object()
        order.is_donated = True
        order.save()
        return redirect("main:dashboard_view")


class UpdateMealOrderStatusView(HybridView):
    model = MealOrder
    permissions = ("Delivery",)

    def get_object(self):
        return self.model.objects.get(pk=self.kwargs["pk"])

    def post(self, request, *args, **kwargs):
        order = self.get_object()
        delivery_status = request.POST.get("delivery_status")
        order.status = delivery_status
        order.save()
        return redirect("main:dashboard_view")
