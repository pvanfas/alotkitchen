from django import forms

from .choices import VALIDITY_CHOICES
from .helper import preference_form_fields
from .models import DeliveryAddress, Preference, SubscriptionRequest
from datetime import datetime


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
        fields = ("first_name", "last_name", "email", "preferred_language", "mobile", "alternate_mobile", "whatsapp_number", "start_date")

        widgets = {
            "first_name": forms.TextInput(attrs={"placeholder": "First Name", "required": "required"}),
            "last_name": forms.TextInput(attrs={"placeholder": "Last Name", "required": "required"}),
            "email": forms.EmailInput(attrs={"placeholder": "Email", "required": "required"}),
            "preferred_language": forms.Select(attrs={"required": "required"}),
            "mobile": forms.TextInput(attrs={"placeholder": "Mobile", "required": "required"}),
            "alternate_mobile": forms.TextInput(attrs={"placeholder": "Alternate Mobile", "required": "required"}),
            "whatsapp_number": forms.TextInput(attrs={"placeholder": "Whatsapp Number", "required": "required"}),
            "start_date": forms.DateInput(attrs={"type": "date", "required": "required", "min": datetime.now().strftime("%Y-%m-%d")}),
        }


class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ("room_no", "floor", "building_name", "street_name", "area", "location", "contact_number", "address_type", "is_default")


class SetDeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ("early_breakfast_address", "breakfast_address", "tiffin_lunch_address", "lunch_address", "dinner_address")
    
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)
        
        # Filter querysets to show only current user's addresses
        if user:
            user_addresses = DeliveryAddress.objects.filter(user=user)
            
            self.fields['early_breakfast_address'].queryset = user_addresses
            self.fields['breakfast_address'].queryset = user_addresses
            self.fields['tiffin_lunch_address'].queryset = user_addresses
            self.fields['lunch_address'].queryset = user_addresses
            self.fields['dinner_address'].queryset = user_addresses
            
            # Set default address if addresses are not already set
            if user_addresses.exists() and not any([
                self.instance.early_breakfast_address,
                self.instance.breakfast_address,
                self.instance.tiffin_lunch_address,
                self.instance.lunch_address,
                self.instance.dinner_address
            ]):
                default_address = user_addresses.first()
                
                if default_address:
                    # Set the same default address for all meal times
                    self.fields['early_breakfast_address'].initial = default_address.pk
                    self.fields['breakfast_address'].initial = default_address.pk
                    self.fields['tiffin_lunch_address'].initial = default_address.pk
                    self.fields['lunch_address'].initial = default_address.pk
                    self.fields['dinner_address'].initial = default_address.pk
                    
                    # Also set empty_label to None to remove the "------" option
                    self.fields['early_breakfast_address'].empty_label = None
                    self.fields['breakfast_address'].empty_label = None
                    self.fields['tiffin_lunch_address'].empty_label = None
                    self.fields['lunch_address'].empty_label = None
                    self.fields['dinner_address'].empty_label = None

class SubscriptionNoteForm(forms.ModelForm):
    class Meta:
        model = Preference
        fields = ("notes",)
        labels = {"notes": "Special Instructions (Allergies, etc.)"}
        widgets = {"notes": forms.Textarea(attrs={"rows": 4})}


class SubscriptionAddressForm(forms.ModelForm):
    class Meta:
        model = SubscriptionRequest
        fields = ()


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
