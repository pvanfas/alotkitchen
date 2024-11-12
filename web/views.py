from django.conf import settings
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe

from main.choices import MEALTYPE_CHOICES
from main.forms import PreferanceForm, SubscriptionAddressForm, SubscriptionNoteForm, SubscriptionRequestForm
from main.models import Area, Combo, SubscriptionPlan, SubscriptionRequest
from main.utils import send_admin_neworder_mail, send_customer_neworder_mail
from users.forms import UserForm


def gen_structured_table_data(combos):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]

    # Initialize table data structure
    table_data = {day: {mealtype: [] for mealtype in mealtypes} for day in days_of_week}

    # Populate table data
    for combo in combos:
        for day in combo["available_days"]:
            if day in table_data:
                data = mark_safe(f'<span>{combo["item_code"]}</span> {combo["name"]}')
                table_data[day][combo["mealtype"]].append(data)

    # Convert nested dictionary into a list of tuples for easier template access
    structured_table_data = [{"day": day, "meals": [{"mealtype": mealtype, "combos": table_data[day][mealtype]} for mealtype in mealtypes]} for day in days_of_week]
    return structured_table_data


def index(request):
    template_name = "web/index.html"
    context = {}
    return render(request, template_name, context)


def page_view(request, slug):
    template_name = "web/page.html"
    area = Area.objects.get(slug=slug)
    context = {"area": area}
    return render(request, template_name, context)


def essential(request):
    tier = "Essential"
    template_name = "web/package.html"
    combos = Combo.objects.filter(tier=tier).values("mealtype", "available_days", "name", "item_code")
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]
    structured_table_data = gen_structured_table_data(combos)
    context = {"structured_table_data": structured_table_data, "mealtypes": mealtypes, "tier": tier}
    return render(request, template_name, context)


def classicveg(request):
    tier = "ClassicVeg"
    template_name = "web/package.html"
    combos = Combo.objects.filter(tier=tier).values("mealtype", "available_days", "name", "item_code")
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]
    structured_table_data = gen_structured_table_data(combos)
    context = {"structured_table_data": structured_table_data, "mealtypes": mealtypes, "tier": tier}
    return render(request, template_name, context)


def classicnonveg(request):
    tier = "ClassicNonVeg"
    template_name = "web/package.html"
    combos = Combo.objects.filter(tier=tier).values("mealtype", "available_days", "name", "item_code")
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]
    structured_table_data = gen_structured_table_data(combos)
    context = {"structured_table_data": structured_table_data, "mealtypes": mealtypes, "tier": tier}
    return render(request, template_name, context)


def standardnonveg(request):
    tier = "StandardNonVeg"
    template_name = "web/package.html"
    combos = Combo.objects.filter(tier=tier).values("mealtype", "available_days", "name", "item_code")
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]
    structured_table_data = gen_structured_table_data(combos)
    context = {"structured_table_data": structured_table_data, "mealtypes": mealtypes, "tier": tier}
    return render(request, template_name, context)


def standardveg(request):
    tier = "StandardVeg"
    template_name = "web/package.html"
    combos = Combo.objects.filter(tier=tier).values("mealtype", "available_days", "name", "item_code")
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]
    structured_table_data = gen_structured_table_data(combos)
    context = {"structured_table_data": structured_table_data, "mealtypes": mealtypes, "tier": tier}
    return render(request, template_name, context)


def customize_menu(request):
    form = PreferanceForm(request.POST or None)
    tier = request.GET.get("tier")
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
    for field in fields:
        form.fields[field].queryset = form.fields[field].queryset.filter(tier=tier)
    template_name = "web/customize_menu.html"
    context = {"form": form}
    if not request.session.session_key:
        request.session.save()

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


def select_plan(request, pk):
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


def get_plans(request):
    tier = request.GET.get("tier")
    validity = request.GET.get("validity")
    plans = SubscriptionPlan.objects.filter(tier=tier, validity=validity).values("id", "name")
    return JsonResponse(list(plans), safe=False)


def test(request):
    send_mail(subject="Test", message="This is a test email", from_email=settings.EMAIL_SENDER, recipient_list=["anfaspv.info@gmail.com"], fail_silently=False)
    return JsonResponse({"status": "success"})
