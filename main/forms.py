from django import forms

from .choices import VALIDITY_CHOICES
from .helper import preference_form_fields
from .models import DeliveryAddress, Preference, SubscriptionRequest

VALIDITY_CHOICES = (("", "-- Select Days --"),) + VALIDITY_CHOICES


class PreferenceForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = preference_form_fields


class ProfileForm(forms.ModelForm):
    mobile_country_code = forms.CharField(max_length=5, required=False)
    alternate_mobile_country_code = forms.CharField(max_length=5, required=False)
    whatsapp_number_country_code = forms.CharField(max_length=5, required=False)

    class Meta:
        model = Preference
        fields = ("first_name", "last_name", "email", "preferred_language", "mobile", "alternate_mobile", "whatsapp_number")

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "required": "required"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "required": "required"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "required": "required"}),
            "preferred_language": forms.Select(attrs={"required": "required"}),
            "mobile": forms.TextInput(attrs={"placeholder": "Mobile", "required": "required"}),
            "alternate_mobile": forms.TextInput(attrs={"placeholder": "Alternate Mobile", "required": "required"}),
            "whatsapp_number": forms.TextInput(attrs={"placeholder": "Whatsapp Number", "required": "required"}),
        }


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ("room_no", "floor", "building_name", "street_name", "area", "location")


class SubscriptionRequestForm(forms.ModelForm):
    select_days = forms.ChoiceField(choices=VALIDITY_CHOICES, label="Select Days")

    class Meta:
        model = SubscriptionRequest
        fields = ("select_days", "plan", "start_date")
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


class SubscriptionRequestApprovalForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = ("area", "delivery_staff", "meal_fee", "no_of_meals")
        labels = {
            "area": "Delivery Zone",
            "delivery_staff": "Delivery Staff",
            "meal_fee": "Meal Fee",
            "no_of_meals": "No of Meals",
        }


class MealOrderUpdateStatusForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = ("status",)
        labels = {"status": "Status"}
        widgets = {"status": forms.Select(attrs={"class": "form-control"})}
