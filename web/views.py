from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView

from main.choices import GROUP_CHOICES, MEALTYPE_CHOICES
from main.forms import PreferenceForm, SubscriptionAddressForm, SubscriptionNoteForm, SubscriptionRequestForm
from main.models import Area, MealCategory, MealPlan, SubscriptionPlan, SubscriptionRequest, SubscriptionSubPlan
from main.utils import send_admin_neworder_mail, send_customer_neworder_mail
from users.forms import UserForm

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
        mealplans = MealPlan.objects.filter(meal_category=meal_category)
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
    plan = subplan.plan
    template_name = "web/customize_meals.html"
    context = {"subplan": subplan, "plan": plan}
    return render(request, template_name, context)


# not verified
def customize_menu(request, pk):
    form = PreferenceForm(request.POST or None)
    plan = SubscriptionPlan.objects.get(pk=pk)
    subplans = plan.get_subs()
    mealtypes = MEALTYPE_CHOICES
    template_name = "web/customize_menu.html"
    context = {"form": form, "plan": plan, "mealtypes": mealtypes, "subplans": subplans}
    if not request.session.session_key:
        request.session.save()

    fields = (
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
    # for field in fields:
    #     form.fields[field].queryset = form.fields[field].queryset.filter(plan=plan)

    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            data.session_id = request.session.session_key
            if request.user.is_authenticated:
                data.user = request.user
            data.save()
            next_url = reverse("web:create_profile") + f"?menu={data.pk}"
            return redirect(next_url)
    return render(request, template_name, context)


def create_profile(request):
    form = UserForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            data = form.save(commit=False)
            mobile = form.cleaned_data.get("mobile")
            alternate_mobile = form.cleaned_data.get("alternate_mobile")
            whatsapp_number = form.cleaned_data.get("whatsapp_number")
            mobile_country_code = form.cleaned_data.get("mobile_country_code")
            alternate_mobile_country_code = form.cleaned_data.get("alternate_mobile_country_code")
            whatsapp_number_country_code = form.cleaned_data.get("whatsapp_number_country_code")
            data.mobile = f"+{mobile_country_code}{mobile}"
            data.alternate_mobile = f"+{alternate_mobile_country_code}{alternate_mobile}"
            data.whatsapp_number = f"+{whatsapp_number_country_code}{whatsapp_number}"
            data.username = f"{mobile_country_code}{mobile}"
            data.is_active = False
            data.save()
            request_obj, _ = SubscriptionRequest.objects.get_or_create(user=data)
            request_obj.stage = "OBJECT_CREATED"
            return redirect("web:select_plan", pk=request_obj.pk)
    template_name = "web/create_profile.html"
    context = {"form": form}
    return render(request, template_name, context)


def select_planx(request, pk):
    instance = SubscriptionRequest.objects.get(pk=pk)
    form = SubscriptionRequestForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            data.stage = "PLAN_SELECTED"
            return redirect("web:select_address", pk=pk)
    template_name = "web/select_plan.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def select_address(request, pk):
    instance = SubscriptionRequest.objects.get(pk=pk)
    form = SubscriptionAddressForm(request.POST or None, instance=instance)
    if "BREAKFAST" not in instance.mealtypes():
        form.fields.pop("breakfast_address_room_no")
        form.fields.pop("breakfast_address_floor")
        form.fields.pop("breakfast_address_building_name")
        form.fields.pop("breakfast_address_street_name")
        form.fields.pop("breakfast_address_area")
        form.fields.pop("breakfast_time")
        form.fields.pop("breakfast_location")
    if "LUNCH" not in instance.mealtypes():
        form.fields.pop("lunch_address_room_no")
        form.fields.pop("lunch_address_floor")
        form.fields.pop("lunch_address_building_name")
        form.fields.pop("lunch_address_street_name")
        form.fields.pop("lunch_address_area")
        form.fields.pop("lunch_time")
        form.fields.pop("lunch_location")
    if "DINNER" not in instance.mealtypes():
        form.fields.pop("dinner_address_room_no")
        form.fields.pop("dinner_address_floor")
        form.fields.pop("dinner_address_building_name")
        form.fields.pop("dinner_address_street_name")
        form.fields.pop("dinner_address_area")
        form.fields.pop("dinner_time")
        form.fields.pop("dinner_location")

    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            data.stage = "ADDRESS_ADDED"
            data.save()
            return redirect("web:confirm_subscription", pk=pk)
    template_name = "web/select_address.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def confirm_subscription(request, pk):
    instance = SubscriptionRequest.objects.get(pk=pk)
    form = SubscriptionNoteForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
            data.stage = "INSTRUCTIONS_ADDED"
            return redirect("web:complete_subscription", pk=pk)
    template_name = "web/confirm_subscription.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def complete_subscription(request, pk):
    template_name = "web/complete_subscription.html"
    instance = SubscriptionRequest.objects.get(pk=pk)
    instance.stage = "COMPLETED"
    instance.completed_at = timezone.now()
    instance.save()
    send_admin_neworder_mail(instance)
    send_customer_neworder_mail(instance)
    context = {}
    return render(request, template_name, context)


def test(request):
    send_mail(subject="Test", message="This is a test email", from_email=settings.EMAIL_SENDER, recipient_list=["anfaspv.info@gmail.com"], fail_silently=False)
    return JsonResponse({"status": "success"})
    send_mail(subject="Test", message="This is a test email", from_email=settings.EMAIL_SENDER, recipient_list=["anfaspv.info@gmail.com"], fail_silently=False)
    return JsonResponse({"status": "success"})
