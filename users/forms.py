from django import forms

from .models import CustomUser as User


class UserForm(forms.ModelForm):
    mobile_country_code = forms.CharField(max_length=5, required=False)
    alternate_mobile_country_code = forms.CharField(max_length=5, required=False)
    whatsapp_number_country_code = forms.CharField(max_length=5, required=False)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "preferred_language", "mobile", "alternate_mobile", "whatsapp_number")

    def clean(self):
        cleaned_data = super().clean()
        mobile = cleaned_data.get("mobile")
        mobile_country_code = cleaned_data.get("mobile_country_code")
        username = f"{mobile_country_code}{mobile}"
        if User.objects.filter(username=username).exists():
            self.add_error("mobile", "Mobile number already registered. Please use a different number or login to your account.")
        return cleaned_data
