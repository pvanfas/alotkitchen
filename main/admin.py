from django.contrib import admin
from django.contrib.auth.models import Group
from registration.models import RegistrationProfile

from main.base import BaseAdmin

from .models import Area, Combo, Item, ItemCategory, MealOrder, PlanGroup, Subscription, SubscriptionPlan, UserAddress

admin.site.unregister(Group)
admin.site.unregister(RegistrationProfile)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(BaseAdmin):
    list_display = ("group", "regular_price", "first_order_price", "validity", "plantype", "is_active")
    list_filter = ("validity", "plantype", "group")


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active")
    list_filter = ("is_active",)
    search_fields = ("user__email",)


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
    list_display = ("name", "category", "price", "is_veg", "available_days")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_veg", "is_active", "available_days")


@admin.register(Combo)
class ComboAdmin(BaseAdmin):
    list_display = ("item_code", "is_veg", "mealtype", "available_days", "available_weeks", "price", "is_default")
    search_fields = ("name", "items")
    list_filter = ("is_veg", "mealtype", "is_active")
    autocomplete_fields = ("items",)


@admin.register(MealOrder)
class MealOrderAdmin(BaseAdmin):
    list_display = ("user", "combo", "quantity", "status")
    search_fields = ("user__email", "combo__name")
    list_filter = ("status",)
    autocomplete_fields = ("user", "combo")


@admin.register(PlanGroup)
class PlanGroupAdmin(BaseAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(UserAddress)
class UserAddressAdmin(BaseAdmin):
    list_display = ("user", "area", "is_default")
    search_fields = ("user__email",)
    list_filter = ("is_default", "is_active")
    autocomplete_fields = ("user", "area")
