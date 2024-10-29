from django import forms

from .choices import TIER_CHOICES, VALIDITY_CHOICES
from .models import SubscriptionRequest

TIER_CHOICES = (("", "-- Select Plan --"),) + TIER_CHOICES
VALIDITY_CHOICES = (("", "-- Select Days --"),) + VALIDITY_CHOICES


class SubscriptionRequestForm(forms.ModelForm):
    select_plan = forms.ChoiceField(choices=TIER_CHOICES, label="Select Plan")
    select_days = forms.ChoiceField(choices=VALIDITY_CHOICES, label="Select Days")

    class Meta:
        model = SubscriptionRequest
        fields = ("select_plan", "select_days", "plan", "start_date")
        widgets = {"start_date": forms.DateInput(attrs={"class": "dateinput form-control", "data-date-start-date": "0d"})}


class SubscriptionAddressForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = (
            "breakfast_address_room_no",
            "breakfast_address_floor",
            "breakfast_address_building_name",
            "breakfast_address_street_name",
            "breakfast_address_area",
            "breakfast_time",
            "breakfast_location",
            "lunch_address_room_no",
            "lunch_address_floor",
            "lunch_address_building_name",
            "lunch_address_street_name",
            "lunch_address_area",
            "lunch_location",
            "lunch_time",
            "dinner_address_room_no",
            "dinner_address_floor",
            "dinner_address_building_name",
            "dinner_address_street_name",
            "dinner_location",
            "dinner_address_area",
            "dinner_time",
            "notes",
        )
        labels = {
            "breakfast_address_room_no": "Room No/Flat",
            "breakfast_address_floor": "Floor",
            "breakfast_address_building_name": "Building Name",
            "breakfast_address_street_name": "Street Name",
            "breakfast_address_area": "Area",
            "lunch_address_room_no": "Room No/Flat",
            "lunch_address_floor": "Floor",
            "lunch_address_building_name": "Building Name",
            "lunch_address_street_name": "Street Name",
            "lunch_address_area": "Area",
            "dinner_address_room_no": "Room No/Flat",
            "dinner_address_floor": "Floor",
            "dinner_address_building_name": "Building Name",
            "dinner_address_street_name": "Street Name",
            "dinner_address_area": "Area",
            "notes": "Special Instructions (Allergies, etc.)",
        }


class SubscriptionNoteForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = ("notes",)
        labels = {"notes": "Special Instructions (Allergies, etc.)"}
        widgets = {"notes": forms.Textarea(attrs={"rows": 4})}
