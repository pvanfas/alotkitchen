from django.shortcuts import render

from main.choices import MEALTYPE_CHOICES
from main.models import Area, Combo


def gen_structured_table_data(combos):
    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    mealtypes = [choice[0] for choice in MEALTYPE_CHOICES]

    # Initialize table data structure
    table_data = {day: {mealtype: [] for mealtype in mealtypes} for day in days_of_week}

    # Populate table data
    for combo in combos:
        for day in combo["available_days"]:
            if day in table_data:
                table_data[day][combo["mealtype"]].append(f"{combo['item_code']}: {combo['name']}")

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
