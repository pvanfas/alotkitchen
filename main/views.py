from datetime import datetime

from django.utils import timezone
from django.views.generic import ListView

from main.mixins import HybridDetailView, HybridListView
from users.models import CustomUser as User
from users.tables import UserTable

from .mixins import HybridTemplateView
from .models import Branch, Combo, ItemCategory, MealOrder, Subscription, SubscriptionPlan, SubscriptionRequest
from .tables import BranchTable, ComboTable, MealOrderDataTable, MealOrderTable, SubscriptionRequestTable

# permissions = ("Administrator", "KitchenManager", "Delivery", "Customer")


def get_week_of_month():
    today = timezone.localdate()
    day_of_month = today.day
    week_number = (day_of_month - 1) // 7 + 1
    return week_number


def get_day_name():
    today = timezone.localdate()
    day_name = today.strftime("%A")  # '%A' formats the day name (e.g., 'Monday')
    return day_name


def get_week_value(n):
    return 2 if n % 2 == 0 else 1


class DashboardView(HybridTemplateView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.usertype == "Customer":
            orders = MealOrder.objects.filter(date=datetime.today(), user=self.request.user, is_active=True)
            context["orders"] = orders
        else:
            context["orders"] = MealOrder.objects.filter(date=datetime.today(), is_active=True)
        return context


class TomorrowOrdersView(HybridTemplateView):
    template_name = "app/main/home.html"
    permissions = ("Administrator", "KitchenManager")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.usertype == "Customer":
            orders = MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), user=self.request.user, is_active=True)
            context["orders"] = orders
        else:
            context["orders"] = MealOrder.objects.filter(date=datetime.today() + timezone.timedelta(days=1), is_active=True)
        return context


class SubscriptionPlanDetailView(HybridDetailView):
    model = SubscriptionPlan
    permissions = ("Customer",)
    template_name = "app/main/subscription_detail.html"


class SubscriptionListView(HybridListView):
    model = Subscription
    filterset_fields = ("user",)
    search_fields = ("user",)
    permissions = ("Customer",)


class SubscriptionDetailView(HybridDetailView):
    model = Subscription
    permissions = ("Customer",)


class BranchListView(HybridListView):
    model = Branch
    filterset_fields = ("name", "code", "address", "phone")
    table_class = BranchTable
    search_fields = ("name", "code", "address", "phone")
    permissions = ("Customer",)


class FeaturedEatsView(HybridTemplateView):
    template_name = "app/main/featured_eats.html"
    permissions = ("Customer",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["week_number"] = get_week_of_month()
        context["day_name"] = get_day_name()
        available_combos = Combo.objects.filter(
            is_active=True,
            available_weeks=get_week_value(get_week_of_month()),
            available_days=get_day_name(),
        )
        context["breakfasts"] = available_combos.filter(is_active=True, mealtype="BREAKFAST")
        context["lunches"] = available_combos.filter(is_active=True, mealtype="LUNCH")
        context["dinners"] = available_combos.filter(is_active=True, mealtype="DINNER")
        return context


class AllEatsView(ListView):
    template_name = "app/main/all_eats.html"
    model = ItemCategory
    context_object_name = "categories"
    permissions = ("Customer",)


class CategoryDetailView(ListView):
    template_name = "app/main/category_detail.html"
    context_object_name = "items"
    model = Combo
    permissions = ("Customer",)

    def get_object(self):
        return ItemCategory.objects.get(pk=self.kwargs["pk"], is_active=True)

    def get_queryset(self):
        return Combo.objects.filter(is_active=True, category=self.get_object())


class HistoryView(HybridListView):
    template_name = "app/main/history.html"
    model = MealOrder
    filterset_fields = ()
    table_class = MealOrderTable
    search_fields = ("combo__name",)
    permissions = ("Customer",)

    def get_queryset(self):
        return MealOrder.objects.filter(user=self.request.user, is_active=True)


class HistoryDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Customer",)


class PricingView(HybridTemplateView):
    template_name = "app/main/pricing.html"
    permissions = ("Customer",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weekly_plans = SubscriptionPlan.objects.filter(is_active=True)
        monthly_plans = SubscriptionPlan.objects.filter(is_active=True)
        context["weekly_plans"] = weekly_plans
        context["monthly_plans"] = monthly_plans
        return context


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
    permissions = ("Administrator", "KitchenManager", "Delivery", "Customer")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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


class ComboListView(HybridListView):
    filterset_fields = ("mealtype", "is_veg")
    search_fields = ("name",)
    permissions = ("Administrator",)
    model = Combo
    title = "Item Master"
    table_class = ComboTable


class ComboDetailView(HybridDetailView):
    model = Combo


class MealOrderListView(HybridListView):
    permissions = ("Administrator",)
    model = MealOrder
    title = "Order Master"
    table_class = MealOrderTable

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class MealOrderDetailView(HybridDetailView):
    model = MealOrder
    permissions = ("Administrator",)


class MealOrderListData(HybridListView):
    model = MealOrder
    permissions = ("Administrator",)
    title = "Order Master Excel"
    table_class = MealOrderDataTable
    template_name = "app/main/mealorder_list_data.html"

    def get_queryset(self):
        return MealOrder.objects.filter(is_active=True)


class SubscriptionRequestListView(HybridListView):
    metadata = {"expand": "newpage"}
    model = SubscriptionRequest
    permissions = ("Administrator",)
    title = "Subscription Requests"
    table_class = SubscriptionRequestTable


class SubscriptionRequestDetailView(HybridDetailView):
    model = SubscriptionRequest
    permissions = ("Administrator",)
    template_name = "app/main/request_detail.html"
