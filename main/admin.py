from django.contrib import admin
from django.contrib.auth.models import Group
from registration.models import RegistrationProfile

from main.base import BaseAdmin

from .models import Combo, Item, ItemCategory, MealOrder, SubscriptionPlan

admin.site.unregister(Group)
admin.site.unregister(RegistrationProfile)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


# @admin.register(Branch)
# class BranchAdmin(BaseAdmin):
#     list_display = ("name", "is_active")
#     search_fields = ("name",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    list_display = ("name", "items_count", "is_active")
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    list_display = ("name", "category", "price", "is_veg", "available_on", "week")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_veg", "is_active", "available_on")


@admin.register(Combo)
class ComboAdmin(BaseAdmin):
    list_display = ("name", "is_veg", "mealtype", "week", "available_on", "is_default")
    search_fields = ("name", "items")
    list_filter = ("is_veg", "mealtype", "is_active")
    autocomplete_fields = ("items",)


@admin.register(MealOrder)
class MealOrderAdmin(BaseAdmin):
    list_display = ("user", "combo", "quantity", "status")
    search_fields = ("user__email", "combo__name")
    list_filter = ("status",)
    autocomplete_fields = ("user", "combo")
