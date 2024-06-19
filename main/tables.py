from main.base import BaseTable

from .models import Branch, District


class DistrictTable(BaseTable):
    class Meta:
        model = District
        fields = ("name", "code")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class BranchTable(BaseTable):
    class Meta:
        model = Branch
        fields = ("name", "code", "address", "phone")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
