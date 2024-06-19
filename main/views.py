from main.mixins import HybridCreateView, HybridDeleteView, HybridDetailView, HybridListView, HybridUpdateView

from .mixins import HybridTemplateView
from .models import Branch, SubscriptionPlan
from .tables import BranchTable, SubscriptionPlanTable


class DashboardView(HybridTemplateView):
    template_name = "app/main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


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
