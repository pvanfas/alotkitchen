from main.mixins import HybridCreateView, HybridDeleteView, HybridDetailView, HybridListView, HybridUpdateView

from .mixins import HybridTemplateView
from .models import Branch, District
from .tables import BranchTable, DistrictTable


class DashboardView(HybridTemplateView):
    template_name = "app/main/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class DistrictListView(HybridListView):
    model = District
    filterset_fields = ("name",)
    table_class = DistrictTable
    search_fields = ("name", "code")


class DistrictCreateView(HybridCreateView):
    model = District


class DistrictDetailView(HybridDetailView):
    model = District


class DistrictUpdateView(HybridUpdateView):
    model = District


class DistrictDeleteView(HybridDeleteView):
    model = District


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
