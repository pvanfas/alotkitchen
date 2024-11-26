from django.contrib import admin
from django.contrib.auth.models import Group
from registration.models import RegistrationProfile

from main.base import BaseAdmin

from .models import Area, ItemCategory, ItemMaster, MealCategory, MealOrder, MealPlan, Preference, Subscription, SubscriptionPlan, SubscriptionRequest, SubscriptionSubPlan

admin.site.unregister(Group)
admin.site.unregister(RegistrationProfile)


class SubscriptionSubPlanInline(admin.TabularInline):
    model = SubscriptionSubPlan
    extra = 0
    exclude = ("is_active",)


@admin.register(MealCategory)
class MealCategoryAdmin(BaseAdmin):
    list_display = ("name", "order", "slug", "description", "is_active")
    search_fields = ("name",)
    list_filter = ()
    list_display_links = ("name", "order", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(BaseAdmin):
    list_display = ("__str__", "validity", "order", "subplans_count", "is_active")
    list_filter = ("validity", "meal_category")
    autocomplete_fields = ("meal_category",)
    inlines = (SubscriptionSubPlanInline,)


@admin.register(Subscription)
class SubscriptionAdmin(BaseAdmin):
    list_display = ("user", "plan", "start_date", "end_date", "is_active", "request")
    list_filter = ("is_active",)
    search_fields = ("user__email",)
    autocomplete_fields = ("user", "plan", "request")


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    list_display = ("name", "is_active", "created")
    search_fields = ("name",)
    list_filter = ("is_active",)


@admin.register(ItemMaster)
class ItemMasterAdmin(BaseAdmin):
    list_display = ("item_code", "name", "group", "mealtype", "category", "is_veg", "price")
    search_fields = ("name", "item_code")
    list_filter = ("price", "is_veg", "group", "category", "mealtype")


@admin.register(MealPlan)
class MealPlanAdmin(BaseAdmin):
    list_display = ("meal_category", "day", "meal_type", "menu_item")
    list_filter = ("is_active", "meal_category", "day", "meal_type")
    autocomplete_fields = ("meal_category", "menu_item")


@admin.register(MealOrder)
class MealOrderAdmin(BaseAdmin):
    list_display = ("user", "item", "quantity", "status", "date", "mealtype", "subscription_plan")
    search_fields = ("user__email", "item__name")
    list_filter = ("status", "subscription_plan", "date")
    autocomplete_fields = ("user", "item", "subscription", "subscription_plan")


@admin.register(Area)
class AreaAdmin(BaseAdmin):
    list_display = ("name", "slug", "is_active", "created")
    search_fields = ("name",)
    list_filter = ("is_active",)
    prepopulated_fields = {"slug": ("name",)}
    autocomplete_fields = ("delivery_staffs",)


@admin.register(SubscriptionRequest)
class SubscriptionRequestAdmin(BaseAdmin):
    list_display = ("user", "plan", "status")
    search_fields = ("user__email",)
    list_filter = ("status",)
    autocomplete_fields = ("user", "plan")


@admin.register(Preference)
class PreferenceAdmin(BaseAdmin):
    list_display = ("user", "is_active")
    list_filter = ("is_active",)
    autocomplete_fields = (
        "user",
        "monday_breakfast",
        "monday_lunch",
        "monday_dinner",
        "tuesday_breakfast",
        "tuesday_lunch",
        "tuesday_dinner",
        "wednesday_breakfast",
        "wednesday_lunch",
        "wednesday_dinner",
        "thursday_breakfast",
        "thursday_lunch",
        "thursday_dinner",
        "friday_breakfast",
        "friday_lunch",
        "friday_dinner",
        "saturday_breakfast",
        "saturday_lunch",
        "saturday_dinner",
        "sunday_breakfast",
        "sunday_lunch",
        "sunday_dinner",
    )
    fieldsets = (
        ("Main", {"fields": ("user", "is_active")}),
        ("Monday", {"fields": ("monday_breakfast", "monday_lunch", "monday_dinner")}),
        ("Tuesday", {"fields": ("tuesday_breakfast", "tuesday_lunch", "tuesday_dinner")}),
        ("Wednesday", {"fields": ("wednesday_breakfast", "wednesday_lunch", "wednesday_dinner")}),
        ("Thursday", {"fields": ("thursday_breakfast", "thursday_lunch", "thursday_dinner")}),
        ("Friday", {"fields": ("friday_breakfast", "friday_lunch", "friday_dinner")}),
        ("Saturday", {"fields": ("saturday_breakfast", "saturday_lunch", "saturday_dinner")}),
        ("Sunday", {"fields": ("sunday_breakfast", "sunday_lunch", "sunday_dinner")}),
    )


@admin.register(SubscriptionSubPlan)
class SubscriptionSubPlanAdmin(BaseAdmin):
    list_display = ("plan", "__str__", "plan_price", "order")
    autocomplete_fields = ("plan",)


# @admin.register(Branch)
# class BranchAdmin(BaseAdmin):
#     list_display = ("name", "is_active")
#     search_fields = ("name",)
