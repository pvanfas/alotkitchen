import operator
import re
from functools import reduce

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.forms import models as model_forms
from django.views.generic import DetailView, FormView, View
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView
from django_filters.views import FilterView
from django_tables2.export.views import ExportMixin
from django_tables2.views import SingleTableMixin


def convert_to_spaces(text):
    result = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    return result


class PermissionMixin(LoginRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if hasattr(self, "permissions"):
            if request.user.is_authenticated:
                if self.request.user.usertype in self.permissions:
                    return super().dispatch(request, *args, **kwargs)
                else:
                    return self.handle_no_permission()
            else:
                return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


class CustomModelFormMixin:
    def get_form_class(self):
        model = getattr(self, "model", None)
        if getattr(self, "fields", None):
            fields = getattr(self, "fields", None)
            return model_forms.modelform_factory(model, fields=fields)
        elif getattr(self, "exclude", None):
            exclude = getattr(self, "exclude", None)
            return model_forms.modelform_factory(model, exclude=exclude)
        else:
            self.fields = "__all__"
            return model_forms.modelform_factory(model, fields=self.fields)
        return super().get_form_class()


class HybridDetailView(PermissionMixin, DetailView):
    template_name = "app/common/object_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title if hasattr(self, "title") else self.object.__str__()
        return context


class HybridCreateView(PermissionMixin, CustomModelFormMixin, CreateView):
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        return self.object.get_list_url()

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title if hasattr(self, "title") else "New " + convert_to_spaces(self.model.__name__)
        return context


class HybridUpdateView(PermissionMixin, CustomModelFormMixin, UpdateView):
    template_name = "app/common/object_form.html"

    def get_success_url(self):
        if self.request.GET.get("next"):
            return self.request.GET.get("next")
        return self.object.get_list_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title if hasattr(self, "title") else "Update " + convert_to_spaces(self.model.__name__)
        return context


class HybridDeleteView(PermissionMixin, DeleteView):
    template_name = "app/common/confirm_delete.html"

    def get_success_url(self):
        return self.object.get_list_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title if hasattr(self, "title") else "Delete " + convert_to_spaces(self.model.__name__)
        return context


class HybridListView(PermissionMixin, ExportMixin, SingleTableMixin, FilterView, ListView):
    table_pagination = {"per_page": 100}
    template_name = "app/common/object_list.html"

    def get_queryset(self):
        search_fields = getattr(self, "search_fields", None)
        if search_fields:
            query = self.request.GET.get("q")
            if query:
                q_list = [Q(**{f"{field}__icontains": query}) for field in search_fields]
                return super().get_queryset().filter(reduce(operator.or_, q_list))
        return super().get_queryset().filter(is_active=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = self.title if hasattr(self, "title") else self.model._meta.verbose_name_plural
        context["can_add"] = True
        context["create_url"] = self.model.get_create_url() if hasattr(self.model, "get_create_url") else None
        context["metadata"] = self.metadata if hasattr(self, "metadata") else {}
        return context


class HybridFormView(PermissionMixin, FormView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "title"):
            context["title"] = self.title
        return context


class HybridTemplateView(PermissionMixin, TemplateView):
    template_name = "app/common/object_view.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "title"):
            context["title"] = self.title
        return context


class HybridView(PermissionMixin, View):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "title"):
            context["title"] = self.title
        return context


class OpenView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if hasattr(self, "title"):
            context["title"] = self.title
        return context
