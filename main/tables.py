from django_tables2 import Table, columns

from main.base import BaseTable

from .models import Branch, ItemMaster, MealOrder, Preference, Subscription, SubscriptionPlan


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
        fields = ("date", "item", "item__mealtype", "subscription_plan", "status")
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
    # Define columns exactly as shown in Excel with correct order and naming
    DocNum = columns.Column(verbose_name="DocNum", accessor="DocNum", orderable=False, empty_values=())
    Series = columns.Column(verbose_name="Series", accessor="Series", orderable=False, empty_values=())
    DocDate = columns.Column(verbose_name="DocDate", accessor="DocDate", orderable=False, empty_values=())
    DocDueDate = columns.Column(verbose_name="DocDueDate", accessor="DocDueDate", orderable=False, empty_values=())
    CardCode = columns.Column(verbose_name="CardCode", accessor="CardCode", orderable=False, empty_values=())
    U_OrderType = columns.Column(verbose_name="U_OrderType", accessor="U_OrderType", orderable=False, empty_values=())
    U_Order_Catg = columns.Column(verbose_name="U_Order_Catg", accessor="U_Order_Catg", orderable=False, empty_values=())
    U_MealType = columns.Column(verbose_name="U_MealType", accessor="U_MealType", orderable=False, empty_values=())
    U_Zone = columns.Column(verbose_name="U_Zone", accessor="U_Zone", orderable=False, empty_values=())
    U_Driver = columns.Column(verbose_name="U_Driver", accessor="U_Driver", orderable=False, empty_values=())
    U_DT = columns.Column(verbose_name="U_DT", accessor="U_DT", orderable=False, empty_values=())
    Comments = columns.Column(verbose_name="Comments", accessor="Comments", orderable=False, empty_values=())
    U_DAddress = columns.Column(verbose_name="U_DAddress", accessor="U_DAddress", orderable=False, empty_values=())
    ParentKey = columns.Column(verbose_name="ParentKey", accessor="ParentKey", orderable=False, empty_values=())  # Note: Changed from DocNum
    LineNum = columns.Column(verbose_name="LineNum", accessor="LineNum", orderable=False, empty_values=())
    Quantity = columns.Column(verbose_name="Quantity", accessor="Quantity", orderable=False, empty_values=())
    ItemCode = columns.Column(verbose_name="ItemCode", accessor="ItemCode", orderable=False, empty_values=())
    PriceAfterVAT = columns.Column(verbose_name="PriceAfterVAT", accessor="PriceAfterVAT", orderable=False, empty_values=())  # Note: Corrected name
    OcrCode = columns.Column(verbose_name="OcrCode", accessor="OcrCode", orderable=False, empty_values=())  # Note: Changed from CostingCode

    class Meta:
        model = MealOrder
        template_name = "django_tables2/table_raw.html"
        # Updated field order to match Excel exactly
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
            "OcrCode",
        )
        attrs = {"class": "table nowrap key-buttons border-bottom table-hover normalcase", "id": "exportTable"}
        sequence = (
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
            "OcrCode",
        )


class PreferenceTable(BaseTable):
    status = columns.TemplateColumn("{{record.get_status_display}}", orderable=False)

    # Add this actions column
    actions = columns.TemplateColumn(
        template_code="""
        {% if record.status == "PENDING" %}
            <button type="button" class="btn btn-sm btn-success" 
                    data-bs-toggle="modal" 
                    data-bs-target="#approveModal" 
                    data-preference-id="{{ record.id }}">
                Approve
            </button>
        {% endif %}
        """,
        verbose_name="Actions",
        orderable=False,
    )

    class Meta:
        model = Preference
        # Add 'actions' to the list of fields to display
        fields = ("subscription_subplan", "first_name", "last_name", "mobile", "completed_at", "start_date", "status", "actions")
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
