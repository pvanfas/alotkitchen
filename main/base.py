from uuid import uuid4

from django.db import models
from django.http import HttpResponseRedirect
from django_tables2 import Table, columns
from import_export.admin import ImportExportActionModelAdmin

from users.models import CustomUser as User

from .actions import mark_active, mark_inactive
from .choices import BOOL_CHOICES
from .functions import generate_fields


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False, blank=True)
    created = models.DateTimeField("Created at", db_index=True, auto_now_add=True)
    updated = models.DateTimeField("Updated at", auto_now=True)
    creator = models.ForeignKey(User, editable=False, blank=True, null=True, related_name="%(app_label)s_%(class)s_creator", on_delete=models.PROTECT)
    is_active = models.BooleanField("Mark as Active", default=True, choices=BOOL_CHOICES)

    class Meta:
        abstract = True
        ordering = ("-created",)

    def get_fields(self):
        return generate_fields(self)

    def delete(self, *args, **kwargs):
        self.is_active = False
        self.save()
        if hasattr(self, "get_list_url") and callable(self.get_list_url):
            return HttpResponseRedirect(self.get_list_url())
        else:
            super().save(*args, **kwargs)


class BaseAdmin(ImportExportActionModelAdmin):
    exclude = ("creator", "is_active")
    list_display = ("__str__", "created", "updated", "is_active")
    list_filter = ("is_active",)
    actions = (mark_active, mark_inactive)
    readonly_fields = ("is_active", "creator", "pk")
    search_fields = ("pk",)

    # def render_change_form(self, request, context, add=False, change=False, form_url="", obj=None):
    #     context.update({"show_save_and_continue": False, "show_save_and_add_another": False})
    #     return super().render_change_form(request, context, add, change, form_url, obj)

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.creator = request.user
        super().save_model(request, obj, form, change)

    class Media:
        css = {"all": ("extra_admin/css/admin.css",)}


class BaseTable(Table):
    pk = columns.Column(visible=False)
    action = columns.TemplateColumn(template_name="app/partials/table_actions.html", orderable=False)
