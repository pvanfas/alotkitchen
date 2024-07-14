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


class FavouritesView(HybridTemplateView):
    template_name = "app/main/favourites.html"


class FeaturedEatsView(HybridTemplateView):
    template_name = "app/main/featured_eats.html"


class WalletView(HybridTemplateView):
    template_name = "app/main/wallet.html"


class PricingView(HybridTemplateView):
    template_name = "app/main/pricing.html"


class ManageAccountView(HybridTemplateView):
    template_name = "app/main/manage_account.html"


class HelpView(HybridTemplateView):
    template_name = "app/main/help.html"
