from main.mixins import HybridCreateView, HybridDeleteView, HybridDetailView, HybridListView, HybridUpdateView

from .mixins import HybridTemplateView
from .models import Branch, SubscriptionPlan
from .tables import SubscriptionPlanTable


class FavouritesView(HybridTemplateView):
    template_name = "app/main/favourites.html"
    permissions = ("Customer",)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class SubscriptionPlanListView(HybridListView):
    model = SubscriptionPlan
    filterset_fields = ()
    table_class = SubscriptionPlanTable
    search_fields = ("name", "code")


class SubscriptionPlanCreateView(HybridCreateView):
    model = SubscriptionPlan


class SubscriptionPlanUpdateView(HybridUpdateView):
    model = SubscriptionPlan


class SubscriptionPlanDeleteView(HybridDeleteView):
    model = SubscriptionPlan


class BranchCreateView(HybridCreateView):
    model = Branch


class BranchDetailView(HybridDetailView):
    model = Branch


class BranchUpdateView(HybridUpdateView):
    model = Branch


class BranchDeleteView(HybridDeleteView):
    model = Branch


class ManageAccountView(HybridTemplateView):
    template_name = "app/main/manage_account.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
