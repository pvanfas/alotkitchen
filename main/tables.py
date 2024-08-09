from django_tables2 import columns

from main.base import BaseTable

from .models import Branch, Combo, MealOrder, SubscriptionPlan, UserAddress


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
    action = columns.TemplateColumn(
        """
        <a class="btn btn-sm btn-light btn-primary-info p-1" href="{{record.get_update_url}}">Edit</a>
        <a class="btn btn-sm btn-light btn-primary-info p-1" href="{{record.get_delete_url}}">Delete</a>
        """
    )
    is_default = columns.BooleanColumn(verbose_name="Default", default=False)

    def render_is_default(self, value):
        return "Yes" if value else "No"

    class Meta:
        model = UserAddress
        fields = ("name", "room_no", "floor", "building_name", "street_name", "mobile", "status", "is_default")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class ComboTable(BaseTable):
    # action = None

    class Meta:
        model = Combo
        fields = ("item_code", "name", "tier", "price", "mealtype", "is_veg", "is_default")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class MealOrderTable(BaseTable):
    action = None

    class Meta:
        model = MealOrder
        fields = ("combo", "combo__mealtype", "date", "quantity", "subscription_plan", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
