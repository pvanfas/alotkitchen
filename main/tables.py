from main.base import BaseTable

from .models import Branch, MealOrder, SubscriptionPlan, UserAddress
from django_tables2 import Table, columns


class SubscriptionPlanTable(BaseTable):
    class Meta:
        model = SubscriptionPlan
        fields = ("name", "code")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class BranchTable(BaseTable):
    class Meta:
        model = Branch
        fields = ("name", "code", "address", "phone")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class MealOrderTable(BaseTable):
    action = None

    class Meta:
        model = MealOrder
        fields = ("combo", "combo__mealtype", "date", "quantity", "subscription_plan", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class UserAddressTable(BaseTable):
    action = columns.TemplateColumn('<a class="btn btn-sm btn-light btn-primary-info" href="{{record.get_update_url}}">Edit</a>')
    class Meta:
        model = UserAddress
        fields = ("name","room_no","floor","building_name","street_name","mobile","status","is_default")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
