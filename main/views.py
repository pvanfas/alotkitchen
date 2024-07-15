from datetime import datetime

from django.utils import timezone

from main.mixins import HybridCreateView, HybridDeleteView, HybridDetailView, HybridListView, HybridUpdateView

from .mixins import HybridTemplateView
from .models import Branch, Combo, MealOrder, SubscriptionPlan, PlanGroup
from .tables import BranchTable, MealOrderTable, SubscriptionPlanTable


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


class SubscriptionPlanListView(HybridListView):
    model = SubscriptionPlan
    filterset_fields = ("name",)
    table_class = SubscriptionPlanTable
    search_fields = ("name", "code")


class SubscriptionPlanCreateView(HybridCreateView):
    model = SubscriptionPlan


class SubscriptionPlanDetailView(HybridDetailView):
    model = SubscriptionPlan


class SubscriptionPlanUpdateView(HybridUpdateView):
    model = SubscriptionPlan


class SubscriptionPlanDeleteView(HybridDeleteView):
    model = SubscriptionPlan


class BranchListView(HybridListView):
    model = Branch
    filterset_fields = ("name", "code", "address", "phone")
    table_class = BranchTable
    search_fields = ("name", "code", "address", "phone")


class BranchCreateView(HybridCreateView):
    model = Branch


class BranchDetailView(HybridDetailView):
    model = Branch


class BranchUpdateView(HybridUpdateView):
    model = Branch


class BranchDeleteView(HybridDeleteView):
    model = Branch


class DashboardView(HybridTemplateView):
    template_name = "app/main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        orders = MealOrder.objects.filter(date=datetime.today(), user=self.request.user, is_active=True)
        context["orders"] = orders
        return context


class FavouritesView(HybridTemplateView):
    template_name = "app/main/favourites.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class FeaturedEatsView(HybridTemplateView):
    template_name = "app/main/featured_eats.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["week_number"] = get_week_of_month()
        context["day_name"] = get_day_name()
        available_combos = Combo.objects.filter(is_active=True, week=get_week_value(get_week_of_month()), available_on=get_day_name())
        context["breakfasts"] = available_combos.filter(is_active=True, mealtype="BREAKFAST")
        context["lunches"] = available_combos.filter(is_active=True, mealtype="LUNCH")
        context["dinners"] = available_combos.filter(is_active=True, mealtype="DINNER")
        return context


class HistoryView(HybridListView):
    template_name = "app/main/history.html"
    model = MealOrder
    filterset_fields = ()
    table_class = MealOrderTable
    search_fields = ("combo__name",)


class HistoryDetailView(HybridDetailView):
    model = MealOrder


class PricingView(HybridTemplateView):
    template_name = "app/main/pricing.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weekly_plans = SubscriptionPlan.objects.filter(is_active=True, plantype="WEEKLY")
        monthly_plans = SubscriptionPlan.objects.filter(is_active=True, plantype="MONTHLY")
        plans = PlanGroup.objects.filter(is_active=True)
        context["weekly_plans"] = weekly_plans
        context["monthly_plans"] = monthly_plans
        context["plans"] = plans
        return context


class ManageAccountView(HybridTemplateView):
    template_name = "app/main/manage_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
