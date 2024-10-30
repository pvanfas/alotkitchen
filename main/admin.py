from django.contrib import admin
from django.contrib.auth.models import Group
from registration.models import RegistrationProfile

from main.base import BaseAdmin

from .models import Area, Combo, ItemCategory, MealOrder, Subscription, SubscriptionPlan, SubscriptionRequest

admin.site.unregister(Group)
admin.site.unregister(RegistrationProfile)


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(BaseAdmin):
    list_display = ("__str__", "validity", "available_mealtypes", "plan_price", "is_active")
    list_filter = ("validity", "tier", "validity", "plan_price")


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active", "request")
    list_filter = ("is_active",)
    search_fields = ("user__email",)
    autocomplete_fields = ("user", "plan", "request")


# @admin.register(Branch)
# class BranchAdmin(BaseAdmin):
#     list_display = ("name", "is_active")
#     search_fields = ("name",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    list_display = ("name", "items_count", "is_active")
    search_fields = ("name",)


@admin.register(Combo)
class ComboAdmin(BaseAdmin):
    list_display = ("item_code", "name", "tier", "is_veg", "mealtype", "available_days", "available_weeks", "price")
    search_fields = ("name", "item_code")
    list_filter = ("tier", "mealtype", "category", "price", "available_days", "available_weeks", "is_veg")


@admin.register(MealOrder)
class MealOrderAdmin(BaseAdmin):
    list_display = ("user", "combo", "quantity", "status", "date", "mealtype", "subscription_plan")
    search_fields = ("user__email", "combo__name")
    list_filter = ("status", "subscription_plan", "date", "combo__mealtype")
    autocomplete_fields = ("user", "combo", "subscription", "subscription_plan")


@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(BaseAdmin):
    list_display = ("user", "plan", "status")
    search_fields = ("user__email",)
    list_filter = ("status",)
    autocomplete_fields = ("user", "plan")
