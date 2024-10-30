from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.core.exceptions import ValidationError

from .models import CustomUser


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            CustomUser.objects.get(username=username)
        except CustomUser.DoesNotExist:
            return username
        raise ValidationError("Username already exists")


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    ordering = ("username",)
    list_display = ("username", "mobile", "usertype", "is_active", "is_staff", "is_superuser", "last_login")
    list_display_links = ("username",)
    readonly_fields = ("last_login", "date_joined", "pk")
    list_filter = ("is_active", "is_staff", "is_superuser", "date_joined", "last_login", "usertype")
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("usertype", "username", "password", "email", "mobile", "first_name", "last_name", "preferred_language", "alternate_mobile", "whatsapp_number")},
        ),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )


admin.site.register(CustomUser, MyUserAdmin)
