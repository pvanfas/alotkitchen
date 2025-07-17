from django_tables2 import Table, columns

from main.base import BaseTable

from .models import Branch, ItemMaster, MealOrder, Subscription, SubscriptionPlan, SubscriptionRequest


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
    status = columns.TemplateColumn("<span class='label label-{{record.flag}} br-3 label label-default mb-0 px-3 py-1'>{{record.get_status_display}}</span>", orderable=False)

    class Meta:
        model = MealOrder
        fields = ("date", "user", "item", "item__mealtype", "subscription_plan", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class CustomerMealOrderTable(BaseTable):
    action = columns.TemplateColumn(template_name="app/partials/customer_order_actions.html", orderable=False)

    class Meta:
        model = MealOrder
        fields = ("item", "item__mealtype", "subscription_plan", "is_donated", "action")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class StandardMealOrderTable(BaseTable):
    status = columns.TemplateColumn("<span class='label label-{{record.flag}} br-3 label label-default mb-0 px-3 py-1'>{{record.get_status_display}}</span>", orderable=False)
    address = columns.TemplateColumn("{{record.get_address}}", orderable=False)
    action = None

    class Meta:
        model = MealOrder
        fields = ("date", "user", "item__mealtype", "item__item_code", "item", "address", "status")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012


class ItemMasterTable(BaseTable):
    # action = None

    class Meta:
        model = ItemMaster
        fields = ("item_code", "name", "meal_category", "price", "mealtype", "is_veg")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noq2


class MealOrderDataTable(Table):

    class Meta:
        model = MealOrder
        template_name = "django_tables2/bootstrap4.html" 
        fields = (
            "DocNum",
            "Series",
            "DocDate",
            "DocDueDate",
            "CardCode",
            "U_OrderType",
            "U_Order_Catg",
            "U_MealType",
            "U_Zone",
            "U_Driver",
            "U_DT",
            "Comments",
            "U_DAddress",
            "ParentKey",
            "LineNum",
            "Quantity",
            "ItemCode",
            "PriceAfterVAT",
            "CostingCode",
            "OcrCode",
        )
        attrs = {"class": "table nowrap key-buttons border-bottom table-hover normalcase", "id": "exportTable"}

class SubscriptionRequestTable(BaseTable):
    status = columns.TemplateColumn("<span class='label label-{{record.flag}} br-3 label label-default mb-0 px-3 py-1'>{{record.get_status_display}}</span>", orderable=False)

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


class DeliveryMealOrderTable(BaseTable):
    action = columns.TemplateColumn(template_name="app/partials/delivery_order_actions.html", orderable=False)
    status = columns.TemplateColumn("<span class='label label-{{record.flag}} br-3 label label-default mb-0 px-3 py-1'>{{record.get_status_display}}</span>", orderable=False)

    class Meta:
        model = MealOrder
        fields = ("user", "item", "item__mealtype", "date", "delivery_time", "status", "action")
        attrs = {"class": "table key-buttons border-bottom table-hover"}  # noqa: RUF012
