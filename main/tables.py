from django_tables2 import Table, columns

from main.base import BaseTable

from .models import Branch, Combo, MealOrder, SubscriptionPlan


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


class ComboTable(BaseTable):
    # action = None

    class Meta:
        model = Combo
        fields = ("item_code", "name", "tier", "price", "mealtype", "is_veg", "is_default")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class MealOrderDataTable(Table):
    DocNum = columns.Column(verbose_name="DocNum")
    Series = columns.Column(verbose_name="Series")
    DocDate = columns.Column(verbose_name="DocDate")
    DocDueDate = columns.Column(verbose_name="DocDueDate")
    CardCode = columns.Column(verbose_name="CardCode")
    U_OrderType = columns.Column(verbose_name="U_OrderType")
    U_Order_Catg = columns.Column(verbose_name="U_Order_Catg")
    U_MealType = columns.Column(verbose_name="U_MealType")
    ParentKey = columns.Column(verbose_name="ParentKey")
    LineNum = columns.Column(verbose_name="LineNum")
    Quantity = columns.Column(verbose_name="Quantity")
    ItemCode = columns.Column(verbose_name="ItemCode")

    class Meta:
        model = MealOrder
        template_name = "django_tables2/table_raw.html"
        fields = ("DocNum", "Series", "DocDate", "DocDueDate", "CardCode", "U_OrderType", "U_Order_Catg", "U_MealType", "ParentKey", "LineNum", "Quantity", "ItemCode")
        attrs = {"class": "table key-buttons border-bottom table-hover normalcase", "id": "exportTable"}  # noqa: RUF012
