from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe

from main.choices import MEALTYPE_CHOICES
from main.forms import SubscriptionAddressForm, SubscriptionNoteForm, SubscriptionRequestForm
from main.models import Area, Combo, SubscriptionPlan, SubscriptionRequest
from users.forms import UserForm
from users.models import CustomUser as User


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


def subscribe(request):
    form = UserForm(request.POST or None)
    if request.method == "POST":
        mobile = request.POST.get("mobile")
        if User.objects.filter(mobile=mobile).exists():
            raise ValidationError("User already exists with this mobile number.")
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
            return redirect("web:select_plan", pk=request_obj.pk)
    template_name = "web/subscribe.html"
    context = {"form": form}
    return render(request, template_name, context)


def select_plan(request, pk):
    instance = SubscriptionRequest.objects.get(pk=pk)
    form = SubscriptionRequestForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            form.save()
            return redirect("web:select_address", pk=pk)
    template_name = "web/select_plan.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def select_address(request, pk):
    instance = SubscriptionRequest.objects.get(pk=pk)
    form = SubscriptionAddressForm(request.POST or None, instance=instance)
    if request.method == "POST":
        if form.is_valid():
            data = form.save()
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
            form.save()
            return redirect("web:complete_subscription", pk=pk)
    template_name = "web/confirm_subscription.html"
    context = {"instance": instance, "form": form}
    return render(request, template_name, context)


def complete_subscription(request, pk):
    template_name = "web/complete_subscription.html"
    context = {}
    return render(request, template_name, context)


def get_plans(request):
    tier = request.GET.get("tier")
    validity = request.GET.get("validity")
    print(tier, validity)
    plans = SubscriptionPlan.objects.filter(tier=tier, validity=validity).values("id", "name")
    return JsonResponse(list(plans), safe=False)
