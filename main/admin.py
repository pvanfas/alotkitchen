from django.contrib import admin
from django.contrib.auth.models import Group
from registration.models import RegistrationProfile

from main.base import BaseAdmin

from .models import Combo, Item, ItemCategory

admin.site.unregister(Group)
admin.site.unregister(RegistrationProfile)


# @admin.register(District)
# class DistrictAdmin(BaseAdmin):
#     list_display = ("name", "is_active")
#     search_fields = ("name",)


# @admin.register(Branch)
# class BranchAdmin(BaseAdmin):
#     list_display = ("name", "is_active")
#     search_fields = ("name",)


@admin.register(ItemCategory)
class ItemCategoryAdmin(BaseAdmin):
    list_display = ("name", "is_active")
    search_fields = ("name",)


@admin.register(Item)
class ItemAdmin(BaseAdmin):
    list_display = ("name", "category", "price", "is_veg", "is_active")
    search_fields = ("name", "category__name")
    list_filter = ("category", "is_veg", "is_active")


@admin.register(Combo)
class ComboAdmin(BaseAdmin):
    list_display = ("name", "price", "is_veg", "mealtype", "is_active", "is_default")
    search_fields = ("name", "items")
    list_filter = ("is_veg", "mealtype", "is_active")
    autocomplete_fields = ("items",)
    list_display_links = ("name", "price", "is_veg", "mealtype", "is_active")
