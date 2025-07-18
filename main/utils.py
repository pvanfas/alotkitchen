from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

from .models import MealOrder, Preference, Subscription
from django.utils import timezone
from datetime import timedelta
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.db import transaction


def send_admin_neworder_mail(instance):
    subject = "ALOT KITCHEN: New Subscription Request"
    message = f"New Subscription Request from {instance.user}"
    template = "email/admin_neworder.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = ["anfaspv.info@gmail.com"]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)


def send_customer_accepted_mail(instance):
    subject = "ALOT KITCHEN: Subscription Request Accepted"
    message = "Your Subscription Request has been accepted"
    template = "email/customer_accepted.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = [instance.user.email]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)


def send_customer_neworder_mail(instance):
    subject = "ALOT KITCHEN: New Subscription Request"
    message = f"New Subscription Request from {instance.user}"
    template = "email/customer_neworder.html"
    html_message = render_to_string(template, {"instance": instance})
    recipient_list = [instance.user.email]
    send_mail(subject, message, settings.EMAIL_SENDER, recipient_list, html_message=html_message)


def create_subscription_from_preference(preference):
    """
    Create subscription and subscription request from approved preference
    """
    plan = preference.subscription_subplan.plan

    # Create subscription request with address information
    subscription_request_data = {
        "user": preference.user,
        "plan": plan,
        "start_date": preference.start_date,
        "status": "APPROVED",
        "stage": "COMPLETED",
        "completed_at": timezone.now(),
        "notes": preference.notes,
        "remarks": preference.remarks,
    }

    # Add address information from preference delivery addresses
    if preference.breakfast_address:
        addr = preference.breakfast_address
        subscription_request_data.update(
            {
                "breakfast_address_room_no": addr.room_no,
                "breakfast_address_floor": addr.floor,
                "breakfast_address_building_name": addr.building_name,
                "breakfast_address_street_name": addr.street_name,
                "breakfast_address_area": addr.area,
                "breakfast_location": addr.location,
            }
        )

    if preference.lunch_address:
        addr = preference.lunch_address
        subscription_request_data.update(
            {
                "lunch_address_room_no": addr.room_no,
                "lunch_address_floor": addr.floor,
                "lunch_address_building_name": addr.building_name,
                "lunch_address_street_name": addr.street_name,
                "lunch_address_area": addr.area,
                "lunch_location": addr.location,
            }
        )

    if preference.dinner_address:
        addr = preference.dinner_address
        subscription_request_data.update(
            {
                "dinner_address_room_no": addr.room_no,
                "dinner_address_floor": addr.floor,
                "dinner_address_building_name": addr.building_name,
                "dinner_address_street_name": addr.street_name,
                "dinner_address_area": addr.area,
                "dinner_location": addr.location,
            }
        )

    # Handle tiffin_lunch address (same as lunch)
    if preference.tiffin_lunch_address:
        addr = preference.tiffin_lunch_address
        subscription_request_data.update(
            {
                "lunch_address_room_no": addr.room_no,
                "lunch_address_floor": addr.floor,
                "lunch_address_building_name": addr.building_name,
                "lunch_address_street_name": addr.street_name,
                "lunch_address_area": addr.area,
                "lunch_location": addr.location,
            }
        )

    # Create or get subscription request
    subscription_request, created = Preference.objects.get_or_create(user=preference.user, plan=plan, start_date=preference.start_date, defaults=subscription_request_data)

    # Create subscription
    subscription = Subscription.objects.create(request=subscription_request, user=preference.user, plan=plan, start_date=preference.start_date)

    return subscription


def bulk_create_meal_orders(preference, subscription):
    """
    Create meal orders for the entire subscription period based on preferences
    """
    orders_to_create = []
    plan = preference.subscription_subplan.plan
    end_date = preference.start_date + timedelta(days=plan.validity)

    # Get available meal types for this subplan
    available_mealtypes = preference.subscription_subplan.available_mealtypes

    # Days of the week
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    # Iterate through each day in the subscription period
    current_date = preference.start_date
    while current_date < end_date:
        day_name = days[current_date.weekday()]  # 0=Monday, 6=Sunday

        # Create orders for each meal type available in the subplan
        for mealtype in available_mealtypes:
            meal_plan = get_meal_plan_for_day_and_type(preference, day_name, mealtype)

            if meal_plan and meal_plan.menu_item:
                # Verify the meal item matches the current meal type
                if meal_plan.menu_item.mealtype == mealtype:
                    orders_to_create.append(MealOrder(user=preference.user, item=meal_plan.menu_item, subscription_plan=plan, subscription=subscription, date=current_date, quantity=1, status="PENDING"))

        current_date += timedelta(days=1)

    # Bulk create all orders
    if orders_to_create:
        MealOrder.objects.bulk_create(orders_to_create, ignore_conflicts=True)

    return len(orders_to_create)


def get_meal_plan_for_day_and_type(preference, day_name, mealtype):
    """
    Get the selected meal plan for a specific day and meal type
    """
    # Map meal types to field suffixes
    mealtype_mapping = {"EARLY_BREAKFAST": "early_breakfast", "BREAKFAST": "breakfast", "TIFFIN_LUNCH": "tiffin_lunch", "LUNCH": "lunch", "DINNER": "dinner"}

    # Get the field suffix for this meal type
    field_suffix = mealtype_mapping.get(mealtype, mealtype.lower())

    # Build the field name: e.g., "monday_breakfast"
    field_name = f"{day_name}_{field_suffix}"

    # Return the meal plan for this day/meal type
    return getattr(preference, field_name, None)


def bulk_create_orders_with_fallback(preference, subscription):
    """
    Enhanced version that includes fallback meals when no specific meal is selected
    """
    orders_to_create = []
    plan = preference.subscription_subplan.plan
    end_date = preference.start_date + timedelta(days=plan.validity)

    # Get available meal types for this subplan
    available_mealtypes = preference.subscription_subplan.available_mealtypes

    # Get fallback meals for this category
    fallback_meals = {}
    for mealtype in available_mealtypes:
        # Look for fallback meals in the meal category
        fallback_meal_plan = plan.meal_category.items.filter(is_fallback=True, menu_item__mealtype=mealtype, menu_item__is_active=True).first()

        if fallback_meal_plan:
            fallback_meals[mealtype] = fallback_meal_plan.menu_item

    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

    current_date = preference.start_date
    while current_date < end_date:
        day_name = days[current_date.weekday()]

        for mealtype in available_mealtypes:
            # Try to get selected meal first
            selected_meal = get_meal_plan_for_day_and_type(preference, day_name, mealtype)

            if selected_meal and selected_meal.menu_item and selected_meal.menu_item.mealtype == mealtype:
                item = selected_meal.menu_item
            elif mealtype in fallback_meals:
                # Use fallback meal if no specific meal selected
                item = fallback_meals[mealtype]
            else:
                # Skip if no meal selected and no fallback available
                continue

            orders_to_create.append(MealOrder(user=preference.user, item=item, subscription_plan=plan, subscription=subscription, date=current_date, quantity=1, status="PENDING"))

        current_date += timedelta(days=1)

    if orders_to_create:
        MealOrder.objects.bulk_create(orders_to_create, ignore_conflicts=True)

    return len(orders_to_create)


def approve_preference_with_fallback(request, pk):
    """
    Enhanced version that includes fallback meals when no specific meal is selected
    """
    preference = get_object_or_404(Preference, pk=pk)

    if preference.status == "APPROVED":
        messages.warning(request, "Preference is already approved.")
        return redirect("main:home_view")

    if not preference.subscription_subplan or not preference.start_date:
        messages.error(request, "Subscription subplan and start date are required.")
        return redirect("main:home_view")

    try:
        with transaction.atomic():
            preference.status = "APPROVED"
            preference.completed_at = timezone.now()
            preference.save()

            subscription = create_subscription_from_preference(preference)
            orders_created = bulk_create_orders_with_fallback(preference, subscription)

            messages.success(request, f"Preference approved successfully! {orders_created} meal orders created.")

    except Exception as e:
        messages.error(request, f"Error approving preference: {str(e)}")
        return redirect("main:home_view")

    return redirect("main:home_view")
