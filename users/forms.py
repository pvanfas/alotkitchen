from django import forms

from .models import CustomUser as User


class UserForm(forms.ModelForm):
    mobile_country_code = forms.CharField(max_length=5, required=False)
    alternate_mobile_country_code = forms.CharField(max_length=5, required=False)
    whatsapp_number_country_code = forms.CharField(max_length=5, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "preferred_language", "mobile", "alternate_mobile", "whatsapp_number")
