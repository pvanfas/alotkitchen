from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from multiselectfield import MultiSelectField

from main.base import BaseModel

MEALTYPE_CHOICES = (("BREAKFAST", "Break Fast"), ("LUNCH", "Lunch"), ("DINNER", "Dinner"), ("ADDON", "Addon"))
WEEK_CHOICES = ((1, "1st & 3rd Week"), (2, "2nd & 4th Week"))
DAY_CHOICES = (
    ("Monday", "Monday"),
    ("Tuesday", "Tuesday"),
    ("Wednesday", "Wednesday"),
    ("Thursday", "Thursday"),
    ("Friday", "Friday"),
    ("Saturday", "Saturday"),
    ("Sunday", "Sunday"),
)
VALIDITY_CHOICES = ((5, "5 Days"), (6, "6 Days"), (7, "7 Days"), (22, "22 Days"), (26, "26 Days"), (30, "30 Days"))
ORDER_STATUS_CHOICES = (("PENDING", "Pending"), ("IN_PREPERATION", "In Preparation"), ("IN_TRANSIT", "In Transit"), ("DELIVERED", "Delivered"), ("CANCELLED", "Cancelled"))
PLANTYPE_CHOICES = (("WEEKLY", "Weekly"), ("MONTHLY", "Monthly"))


class ItemCategory(BaseModel):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to="categories", height_field=None, width_field=None, max_length=None)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Item Category")
        verbose_name_plural = _("Item Categories")

    def items_count(self):
        return self.items.count()

    def __str__(self):
        return self.name


class Item(BaseModel):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="items/images/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    available_on = MultiSelectField(max_length=200, choices=DAY_CHOICES, null=True, blank=True)
    week = models.PositiveIntegerField(choices=WEEK_CHOICES)
    is_veg = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Item")
        verbose_name_plural = _("Items")

    def __str__(self):
        return self.name


class Combo(BaseModel):
    items = models.ManyToManyField(Item, related_name="combos")
    image = models.ImageField(upload_to="items/images/", blank=True, null=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    mealtype = models.CharField(max_length=200, choices=MEALTYPE_CHOICES)
    week = models.PositiveIntegerField(choices=WEEK_CHOICES)
    available_on = models.CharField(max_length=200, choices=DAY_CHOICES)
    is_veg = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)

    class Meta:
        ordering = ("week", "available_on", "mealtype")
        verbose_name = _("Combo")
        verbose_name_plural = _("Combos")

    def get_combo_name(self):
        return ", ".join(item.name for item in self.items.all())

    def save(self, *args, **kwargs):
        if not self.pk:
            self.name = "Unnamed Combo"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


@receiver(m2m_changed, sender=Combo.items.through)
def update_combo_name(sender, instance, action, reverse, pk_set, **kwargs):
    if action == "post_add" or action == "post_remove" or action == "post_clear":
        instance.name = instance.get_combo_name()
        instance.save()


class SubscriptionPlan(BaseModel):
    name = models.CharField(max_length=200)
    validity = models.IntegerField(choices=VALIDITY_CHOICES)
    plantype = models.CharField(max_length=200, choices=PLANTYPE_CHOICES)
    regular_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    first_order_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    bi_monthly_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Subscription Plan")
        verbose_name_plural = _("Subscription Plans")

    def get_absolute_url(self):
        return reverse_lazy("main:subscriptionplan_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:subscriptionplan_list")

    @staticmethod
    def get_create_url():
        return reverse_lazy("main:subscriptionplan_create")

    def get_update_url(self):
        return reverse_lazy("main:subscriptionplan_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:subscriptionplan_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


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

    @staticmethod
    def get_create_url():
        return reverse_lazy("main:branch_create")

    def get_update_url(self):
        return reverse_lazy("main:branch_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:branch_delete", kwargs={"pk": self.pk})

    def __str__(self):
        return str(self.name)


class MealOrder(BaseModel):
    user = models.ForeignKey("users.CustomUser", on_delete=models.CASCADE, related_name="usermeals")
    combo = models.ForeignKey(Combo, on_delete=models.CASCADE, related_name="combomeals")
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, related_name="mealsplan")
    date = models.DateField()
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=200, default="PENDING", choices=ORDER_STATUS_CHOICES)

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

    class Meta:
        ordering = ("date",)
        verbose_name = _("Meal")
        verbose_name_plural = _("Meals")

    def __str__(self):
        return f"{self.combo} - {self.date}"
