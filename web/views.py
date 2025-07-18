from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from main.choices import GROUP_CHOICES, MEALTYPE_CHOICES
from main.forms import DeliveryAddressForm, PreferenceForm, ProfileForm, SetDeliveryAddressForm, SubscriptionNoteForm
from main.models import Area, DeliveryAddress, MealCategory, MealPlan, Preference, SubscriptionPlan, SubscriptionSubPlan

from .serializers import MealPlanSerializer, SubscriptionPlanSerializer


class SubscriptionPlanListView(APIView):
    def get(self, request, pk):
        meal_category = get_object_or_404(MealCategory, pk=pk)
        plans = SubscriptionPlan.objects.filter(meal_category=meal_category)
        serializer = SubscriptionPlanSerializer(plans, many=True)
        return Response(serializer.data)


class SubscriptionPlanMealPlanListView(APIView):
    def get(self, request, pk):
        meal_category = get_object_or_404(MealCategory, pk=pk)
        mealplans = MealPlan.objects.filter(meal_category=meal_category, is_fallback=False)
        serializer = MealPlanSerializer(mealplans, many=True)
        return Response(serializer.data)


def index(request):
    template_name = "web/index.html"
    meal_categories = MealCategory.objects.filter(is_active=True)
    context = {"meal_categories": meal_categories}
    return render(request, template_name, context)


def page_view(request, slug):
    template_name = "web/page_view.html"
    area = get_object_or_404(Area, slug=slug)
    meal_categories = MealCategory.objects.filter(is_active=True)
    context = {"meal_categories": meal_categories, "area": area}
    return render(request, template_name, context)


def select_plan(request, slug):
    template_name = "web/select_plan.html"
    meal_category = get_object_or_404(MealCategory, slug=slug)
    grouped_meal_categories = {group: list(MealCategory.objects.filter(is_active=True, group=group).order_by("order")) for group, _ in GROUP_CHOICES}
    context = {"meal_category": meal_category, "groups": GROUP_CHOICES, "grouped_meal_categories": grouped_meal_categories}
    return render(request, template_name, context)


def select_meals(request, pk):
    plan = get_object_or_404(SubscriptionPlan, pk=pk)
    subplans = plan.get_subs()
    mealtypes = MEALTYPE_CHOICES
    template_name = "web/select_meals.html"
    context = {"plan": plan, "mealtypes": mealtypes, "subplans": subplans}
    return render(request, template_name, context)


def customize_meals(request, pk):
    subplan = get_object_or_404(SubscriptionSubPlan, pk=pk)
    mealtypes = list(subplan.available_mealtypes)
    template_name = "web/customize_meals.html"
    request.session.save() if not request.session.session_key else None
    form = PreferenceForm(request.POST or None)
    for field in form.fields:
        form.fields[field].queryset = form.fields[field].queryset.filter(meal_category=subplan.plan.meal_category)
    context = {"subplan": subplan, "plan": subplan.plan, "available_mealtypes": mealtypes, "form": form}
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.session_id = request.session.session_key
            data.user = request.user if request.user.is_authenticated else None
            data.subscription_subplan = subplan
            data.save()
            return redirect("web:create_profile", pk=data.pk)
    return render(request, template_name, context)


def create_profile(request, pk):
    template_name = "web/create_profile.html"

    # Attempt to retrieve an existing Preference instance
    preference = get_object_or_404(Preference, pk=pk)

    # Bind the form to the instance (for editing)
    form = ProfileForm(request.POST or None, instance=preference)

    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)

            def format_number(country_code, number):
                if country_code and number:
                    return f"+{country_code}{number}"
                return None

            data.mobile = format_number(
                form.cleaned_data.get("mobile_country_code"),
                form.cleaned_data.get("mobile")
            )
            data.alternate_mobile = format_number(
                form.cleaned_data.get("alternate_mobile_country_code"),
                form.cleaned_data.get("alternate_mobile")
            )
            data.whatsapp_number = format_number(
                form.cleaned_data.get("whatsapp_number_country_code"),
                form.cleaned_data.get("whatsapp_number")
            )

            data.save()
            return redirect("web:select_address", pk=pk)
        else:
            print(form.errors)

    context = {"form": form}
    return render(request, template_name, context)


def select_address(request, pk):
    instance = Preference.objects.get(pk=pk)
    # addresses = instance.get_addresses()
    addresses = DeliveryAddress.objects.filter(preference = instance)
    
    # Create form without instance since we're creating a new DeliveryAddress
    form = DeliveryAddressForm(request.POST or None)
    
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.preference = instance  # Use the actual field name from the model
            data.session_id = instance.session_id
            data.user = request.user if request.user.is_authenticated else None
            if data.is_default:
                # Set all other addresses to not default if this one is set as default
                DeliveryAddress.objects.filter(preference=instance, is_default=True).update(is_default=False)
            data.save()
            return redirect("web:select_address", pk=pk)
    
    template_name = "web/select_address.html"
    context = {"instance": instance, "form": form, "addresses": addresses}
    return render(request, template_name, context)


def set_delivery_address(request, pk):
    instance = Preference.objects.get(pk=pk)
    addresses = DeliveryAddress.objects.filter(preference = instance)
    form = SetDeliveryAddressForm(request.POST or None, instance=instance)
    
    # filter the queryset to only include addresses for the current preference
    form.fields['early_breakfast_address'].queryset = addresses
    form.fields['breakfast_address'].queryset = addresses
    form.fields['tiffin_lunch_address'].queryset = addresses
    form.fields['lunch_address'].queryset = addresses
    form.fields['dinner_address'].queryset = addresses

    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.preference = instance
            data.session_id = instance.session_id
            data.user = request.user if request.user.is_authenticated else None
            data.save()

            return redirect("web:confirm_subscription", pk=pk)
    template_name = "web/set_delivery_address.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def confirm_subscription(request, pk):
    instance = Preference.objects.get(pk=pk)
    form = SubscriptionNoteForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("web:complete_subscription", pk=pk)
    template_name = "web/confirm_subscription.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def complete_subscription(request, pk):
    template_name = "web/complete_subscription.html"
    instance = Preference.objects.get(pk=pk)
    instance.status = "PENDING"
    instance.completed_at = timezone.now()
    instance.save()
    # send_admin_neworder_mail(instance)
    # send_customer_neworder_mail(instance)
    context = {}
    return render(request, template_name, context)
