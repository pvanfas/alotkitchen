from django_tables2 import Table, columns

from main.base import BaseTable

from .models import Branch, Combo, MealOrder, Subscription, SubscriptionPlan, SubscriptionRequest


class SubscriptionTable(BaseTable):
    class Meta:
        model = Subscription
        fields = ("user", "plan", "start_date", "end_date")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


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
    class Meta:
        model = MealOrder
        fields = ("date", "user", "combo", "combo__mealtype", "subscription_plan", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class StandardMealOrderTable(BaseTable):
    address = columns.TemplateColumn("{{record.get_address}}", orderable=False)
    action = None

    class Meta:
        model = MealOrder
        fields = ("date", "user", "combo__mealtype", "combo__item_code", "combo", "address", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class ComboTable(BaseTable):
    # action = None

    class Meta:
        model = Combo
        fields = ("item_code", "name", "tier", "price", "mealtype", "is_veg")
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


class SubscriptionRequestTable(BaseTable):
    class Meta:
        model = SubscriptionRequest
        fields = ("user", "plan", "start_date", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class StandardSubscriptionTable(BaseTable):
    action = None
    address = columns.TemplateColumn(template_name="app/partials/address_preview.html", orderable=False)

    class Meta:
        model = Subscription
        fields = ("user", "plan", "start_date", "end_date")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
