from django.db import models
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from main.base import BaseModel

from .choices import (
    BREAKFAST_DELIVERY_CHOICES,
    DAY_CHOICES,
    DINNER_DELIVERY_CHOICES,
    GROUP_CHOICES,
    LUNCH_DELIVERY_CHOICES,
    MEALTYPE_CHOICES,
    ORDER_STATUS_CHOICES,
    TIER_CHOICES,
    VALIDITY_CHOICES,
    WEEK_CHOICES,
)


def get_week_number(date):
    day_of_month = date.day
    week_number = (day_of_month - 1) // 7 + 1
    return 2 if week_number % 2 == 0 else 1


class MealCategory(BaseModel):
    order = models.PositiveIntegerField(default=1)
    group = models.CharField(max_length=200, choices=GROUP_CHOICES)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to="mealcategories/image")
    description = models.TextField(blank=True, null=True)
    brochure = models.FileField(upload_to="mealcategories/brochure/", blank=True, null=True)

    class Meta:
        ordering = ("order",)
        verbose_name = _("Meal Category")
        verbose_name_plural = _("Meal Categories")

    def get_absolute_url(self):
        return reverse_lazy("web:mealcategory_detail", kwargs={"slug": self.slug})

    def __str__(self):
        return self.name


class Area(BaseModel):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    delivery_staffs = models.ManyToManyField("users.CustomUser", related_name="delivery_areas", limit_choices_to={"usertype": "Delivery"}, blank=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Area")
        verbose_name_plural = _("Areas")

    def __str__(self):
        return self.name


class Combo(BaseModel):
    meal_category = models.ForeignKey(MealCategory, on_delete=models.CASCADE, related_name="combos", blank=True, null=True)
    tier = models.CharField(max_length=200, choices=TIER_CHOICES)
    mealtype = models.CharField(max_length=200, choices=MEALTYPE_CHOICES)
    image = models.ImageField(upload_to="items/images/", blank=True, null=True)
    name = models.CharField(max_length=200)
    item_code = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    available_days = MultiSelectField(max_length=200, choices=DAY_CHOICES)
    available_weeks = MultiSelectField(max_length=200, choices=WEEK_CHOICES)
    is_veg = models.BooleanField(default=True)

    class Meta:
        ordering = ("available_weeks", "available_days", "mealtype")
        verbose_name = _("Item Master")
        verbose_name_plural = _("Item Masters")

    def get_absolute_url(self):
        return reverse_lazy("main:combo_detail", kwargs={"pk": self.pk})

    def get_combo_name(self):
        return ", ".join(item.name for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = "Unnamed Combo"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Preferance(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="preferances", blank=True, null=True)
    session_id = models.CharField(max_length=200, blank=True, null=True)
    monday_breakfast = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="monday_breakfast", blank=True, null=True, limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Monday"}
    )
    monday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="monday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Monday"}
    )
    monday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="monday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Monday"}
    )

    tuesday_breakfast = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="tuesday_breakfast", blank=True, null=True, limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Tuesday"}
    )
    tuesday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="tuesday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Tuesday"}
    )
    tuesday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="tuesday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Tuesday"}
    )

    wednesday_breakfast = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name="wednesday_breakfast",
        blank=True,
        null=True,
        limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Wednesday"},
    )
    wednesday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="wednesday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Wednesday"}
    )
    wednesday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="wednesday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Wednesday"}
    )

    thursday_breakfast = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name="thursday_breakfast",
        blank=True,
        null=True,
        limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Thursday"},
    )
    thursday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="thursday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Thursday"}
    )
    thursday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="thursday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Thursday"}
    )

    friday_breakfast = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="friday_breakfast", blank=True, null=True, limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Friday"}
    )
    friday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="friday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Friday"}
    )
    friday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="friday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Friday"}
    )

    saturday_breakfast = models.ForeignKey(
        Combo,
        on_delete=models.CASCADE,
        related_name="saturday_breakfast",
        blank=True,
        null=True,
        limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Saturday"},
    )
    saturday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="saturday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Saturday"}
    )
    saturday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="saturday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Saturday"}
    )

    sunday_breakfast = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="sunday_breakfast", blank=True, null=True, limit_choices_to={"mealtype": "BREAKFAST", "available_days__contains": "Sunday"}
    )
    sunday_lunch = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="sunday_lunch", blank=True, null=True, limit_choices_to={"mealtype": "LUNCH", "available_days__contains": "Sunday"}
    )
    sunday_dinner = models.ForeignKey(
        Combo, on_delete=models.CASCADE, related_name="sunday_dinner", blank=True, null=True, limit_choices_to={"mealtype": "DINNER", "available_days__contains": "Sunday"}
    )

    class Meta:
        ordering = ("user",)
        verbose_name = _("Preferance")
        verbose_name_plural = _("Preferances")

    def __str__(self):
        return f"{self.user}"


class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=200)
    tier = models.CharField(max_length=200, choices=TIER_CHOICES)
    available_mealtypes = MultiSelectField(max_length=200, choices=MEALTYPE_CHOICES)
    validity = models.IntegerField(choices=VALIDITY_CHOICES)
    plan_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ("tier", "validity", "name")
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")

    def get_menu_url(self):
        mapping = {
            "Essential": "web:essential",
            "ClassicVeg": "web:classicveg",
            "ClassicNonVeg": "web:classicnonveg",
            "StandardNonVeg": "web:standardnonveg",
            "StandardVeg": "web:standardveg",
        }
        return reverse(mapping[self.tier])

    # def get_absolute_url(self):
    #     return reverse_lazy("main:subscriptionplan_detail", kwargs={"pk": self.pk})

    # @staticmethod
    # def get_list_url():
    #     return reverse_lazy("main:subscriptionplan_list")

    # @staticmethod
    # def get_create_url():
    #     return reverse_lazy("main:subscriptionplan_create")

    # def get_update_url(self):
    #     return reverse_lazy("main:subscriptionplan_update", kwargs={"pk": self.pk})

    # def get_delete_url(self):
    #     return reverse_lazy("main:subscriptionplan_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.tier} - ({self.name}) - {self.validity} Days"


class Subscription(BaseModel):
    request = models.ForeignKey("main.SubscriptionRequest", on_delete=models.CASCADE, related_name="subscription_requests")
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="subscriptions")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscription_plan")
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _("Subscription")
        verbose_name_plural = _("Subscriptions")

    def get_absolute_url(self):
        return reverse_lazy("main:subscription_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:subscription_list")

    def save(self, *args, **kwargs):
        self.end_date = self.start_date + timezone.timedelta(days=self.plan.validity)
        create_orders(self)
        super().save(*args, **kwargs)

    # @staticmethod
    # def get_create_url():
    #     return reverse_lazy("main:subscription_create")

    # def get_update_url(self):
    #     return reverse_lazy("main:subscription_update", kwargs={"pk": self.pk})

    # def get_delete_url(self):
    #     return reverse_lazy("main:subscription_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.start_date}"


class Branch(BaseModel):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(max_length=200, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Branch")
        verbose_name_plural = _("Branches")

    def get_absolute_url(self):
        return reverse_lazy("main:branch_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:branch_list")

    # @staticmethod
    # def get_create_url():
    #     return reverse_lazy("main:branch_create")

    # def get_update_url(self):
    #     return reverse_lazy("main:branch_update", kwargs={"pk": self.pk})

    # def get_delete_url(self):
    #     return reverse_lazy("main:branch_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


class MealOrder(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="usermeals")
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name="combomeals")
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="mealsplan")
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name="meals")
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=200, default="PENDING", choices=ORDER_STATUS_CHOICES)
    is_donated = models.BooleanField(default=False)

    def flag(self):
        data = {
            "PENDING": "warning",
            "IN_PREPERATION": "info",
            "IN_TRANSIT": "primary",
            "DELIVERED": "success",
            "CANCELLED": "danger",
        }
        return data[self.status]

    def get_absolute_url(self):
        return reverse("main:history_detail_view", kwargs={"pk": self.pk})

    def get_address(self):
        req = self.subscription.request
        print(self.subscription)
        if self.combo.mealtype == "BREAKFAST":
            return f"Room: {req.breakfast_address_room_no}, {req.breakfast_address_floor}, {req.breakfast_address_building_name}, {req.breakfast_address_street_name}, {req.breakfast_address_area}"
        if self.combo.mealtype == "LUNCH":
            return f"Room: {req.lunch_address_room_no}, {req.lunch_address_floor}, {req.lunch_address_building_name}, {req.lunch_address_street_name}, {req.lunch_address_area}"
        if self.combo.mealtype == "DINNER":
            return (
                f"Room: {req.dinner_address_room_no}, {req.dinner_address_floor}, {req.dinner_address_building_name}, {req.dinner_address_street_name}, {req.dinner_address_area}"
            )
        if self.combo.mealtype == "TIFFIN":
            return f"Room: {req.lunch_address_room_no}, {req.lunch_address_floor}, {req.lunch_address_building_name}, {req.lunch_address_street_name}, {req.lunch_address_area}"

    class Meta:
        ordering = ("date",)
        verbose_name = _("Meal Order")
        verbose_name_plural = _("Meal Orders")

    def mealtype(self):
        return self.combo.mealtype

    def DocNum(self):
        return " "

    def Series(self):
        return "70"

    def DocDate(self):
        return self.date.strftime("%Y%m%d")

    def DocDueDate(self):
        return self.date.strftime("%Y%m%d")

    def CardCode(self):
        return self.user.username

    def U_OrderType(self):
        if self.combo.is_veg:
            return "Veg"
        return "Non Veg"

    def U_Order_Catg(self):
        return self.combo.tier

    def U_MealType(self):
        return self.combo.mealtype.capitalize()

    def U_Zone(self):
        return self.subscription.request.area

    def U_Driver(self):
        return self.subscription.request.delivery_staff

    def U_DT(self):
        if self.combo.mealtype == "BREAKFAST":
            value = self.subscription.request.get_breakfast_time_display()
        if self.combo.mealtype == "LUNCH":
            value = self.subscription.request.get_lunch_time_display()
        if self.combo.mealtype == "DINNER":
            value = self.subscription.request.get_dinner_time_display()
        if self.combo.mealtype == "TIFFIN_LUNCH":
            value = self.subscription.request.get_lunch_time_display()
        if value:
            return value.split("to")[0]
        else:
            return ""

    def map(self):
        if self.combo.mealtype == "BREAKFAST":
            return self.subscription.request.breakfast_location
        if self.combo.mealtype == "LUNCH":
            return self.subscription.request.lunch_location
        if self.combo.mealtype == "DINNER":
            return self.subscription.request.dinner_location
        if self.combo.mealtype == "TIFFIN_LUNCH":
            return self.subscription.request.lunch_location
        return None

    def delivery_time(self):
        return self.U_DT()

    def ParentKey(self):
        return " "

    def LineNum(self):
        return 0

    def Quantity(self):
        return self.quantity

    def ItemCode(self):
        return self.combo.item_code

    def PriceAfterVAT(self):
        return self.combo.price

    def __str__(self):
        return f"{self.combo} - {self.date}"


class SubscriptionRequest(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="subscription_requests")
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="subscription_requests", blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)

    breakfast_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_floor = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    breakfast_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="breakfast_address_area", blank=True, null=True)
    breakfast_time = models.CharField("Delivery Time (Breakfast)", max_length=200, choices=BREAKFAST_DELIVERY_CHOICES, default="0900:0930")
    breakfast_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    lunch_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_floor = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    lunch_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="lunch_address_area", blank=True, null=True)
    lunch_time = models.CharField("Delivery Time (Lunch", max_length=200, choices=LUNCH_DELIVERY_CHOICES, default="1230:1300")
    lunch_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    dinner_address_room_no = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_floor = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_building_name = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_street_name = models.CharField(max_length=200, blank=True, null=True)
    dinner_address_area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name="dinner_address_area", blank=True, null=True)
    dinner_time = models.CharField("Delivery Time (Dinner)", max_length=200, choices=DINNER_DELIVERY_CHOICES, default="2100:2130")
    dinner_location = models.URLField("Location Map Link", max_length=200, blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=200, default="PENDING", choices=(("PENDING", "Pending"), ("APPROVED", "Approved"), ("REJECTED", "Rejected")))
    remarks = models.TextField(blank=True, null=True)
    stage = models.CharField(
        max_length=200,
        default="OBJECT_CREATED",
        choices=(("OBJECT_CREATED", "OBJECT_CREATED"), ("PLAN_SELECTED", "PLAN_SELECTED"), ("ADDRESS_ADDED", "ADDRESS_ADDED"), ("COMPLETED", "COMPLETED")),
    )
    completed_at = models.DateTimeField(blank=True, null=True)

    approved_by = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="approved_requests", blank=True, null=True)
    approved_at = models.DateTimeField(blank=True, null=True)
    area = models.ForeignKey("main.Area", verbose_name=_("Zone"), on_delete=models.CASCADE, blank=True, null=True)
    delivery_staff = models.ForeignKey(
        "users.CustomUser", on_delete=models.CASCADE, related_name="driver_requests", blank=True, null=True, limit_choices_to={"usertype": "Delivery"}
    )
    meal_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    no_of_meals = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ("start_date",)
        verbose_name = _("Subscription Request")
        verbose_name_plural = _("Subscription Requests")

    def get_absolute_url(self):
        return reverse("main:subscriptionrequest_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse("main:subscriptionrequest_list")

    def get_update_url(self):
        return reverse("main:subscriptionrequest_update", kwargs={"pk": self.pk})

    def get_approve_url(self):
        return reverse("main:subscriptionrequest_approve", kwargs={"pk": self.pk})

    def get_reject_url(self):
        return reverse("main:subscriptionrequest_reject", kwargs={"pk": self.pk})

    def get_print_url(self):
        return reverse("main:subscriptionrequest_print", kwargs={"pk": self.pk})

    def mealtypes(self):
        if self.plan:
            return set(self.plan.available_mealtypes)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.start_date}"


def create_orders(subscription):
    for i in range(subscription.plan.validity):
        date = subscription.start_date + timezone.timedelta(days=i)
        day_of_week = date.strftime("%A")
        mealtypes = list(subscription.plan.available_mealtypes)
        week_number = get_week_number(date)
        combos = Combo.objects.filter(
            is_active=True, tier=subscription.plan.tier, mealtype__in=mealtypes, available_days__contains=day_of_week, available_weeks__contains=str(week_number)
        )
        for combo in combos:
            for meal in mealtypes:
                MealOrder.objects.get_or_create(user=subscription.user, combo=combo, subscription=subscription, subscription_plan=subscription.plan, date=date)
    return True
