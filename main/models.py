from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

from main.base import BaseModel

MEALTYPE_CHOICES = (("BREAKFAST", "Break Fast"), ("LUNCH", "Lunch"), ("DINNER", "Dinner"))


class ItemCategory(BaseModel):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Item Category")
        verbose_name_plural = _("Item Categories")

    def __str__(self):
        return self.name


class Item(BaseModel):
    category = models.ForeignKey(ItemCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="items/images/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
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
    is_veg = models.BooleanField(default=True)
    is_default = models.BooleanField(default=True)

    class Meta:
        ordering = ("name",)
        verbose_name = _("Combo")
        verbose_name_plural = _("Combos")

    def get_combo_name(self):
        return ", ".join(item.name for item in self.items.all())

    def clean(self):
        existing_combos = Combo.objects.filter(items__in=self.items.all()).distinct()
        for combo in existing_combos:
            if self.pk and combo.pk == self.pk:
                continue  # Skip current instance being edited
            if set(combo.items.all()) == set(self.items.all()):
                raise ValidationError("This combination of items already exists in another Combo.")

    def save(self, *args, **kwargs):
        self.clean()
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


class District(BaseModel):
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ("name",)
        verbose_name = _("District")
        verbose_name_plural = _("Districts")

    def get_absolute_url(self):
        return reverse_lazy("main:district_detail", kwargs={"pk": self.pk})

    @staticmethod
    def get_list_url():
        return reverse_lazy("main:district_list")

    @staticmethod
    def get_create_url():
        return reverse_lazy("main:district_create")

    def get_update_url(self):
        return reverse_lazy("main:district_update", kwargs={"pk": self.pk})

    def get_delete_url(self):
        return reverse_lazy("main:district_delete", kwargs={"pk": self.pk})

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
