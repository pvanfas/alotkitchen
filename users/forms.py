from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout
from django import forms
from django.contrib.auth.hashers import make_password

from .models import CustomUser as User


class UserForm(forms.ModelForm):
    country_code = forms.CharField(max_length=5, required=True, label="Country Code", help_text="e.g., +91")
    username = forms.CharField(max_length=150, required=True, label="Username", help_text="Enter a unique username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    password_confirm = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = (
            "username",
            "mobile",
            "email",
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "post"
        self.helper.layout = Layout(
            Field("username", css_class="form-control"),
            Field("country_code", css_class="form-control"),
            Field("mobile", css_class="form-control"),
            Field("email", css_class="form-control"),
            Field("password", css_class="form-control"),
            Field("password_confirm", css_class="form-control"),
        )

    def clean(self):
        cleaned_data = super().clean()
        mobile = cleaned_data.get("mobile")
        country_code = cleaned_data.get("country_code")
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get("password_confirm")

        if password and password != password_confirm:
            self.add_error("password_confirm", "Passwords do not match.")

        # Check if username already exists
        if username and User.objects.filter(username=username).exists():
            self.add_error("username", "Username already exists.")

        # Check mobile number (with country code)
        mobile_with_country = f"{country_code}{mobile}"
        if User.objects.filter(username=mobile_with_country).exists():
            self.add_error("mobile", "Mobile number already registered.")

        if User.objects.filter(email=email).exists():
            self.add_error("email", "Email is already in use.")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        self.cleaned_data.get("country_code")
        mobile = self.cleaned_data.get("mobile")
        username = self.cleaned_data.get("username")

        # Use the provided username instead of generating one
        user.username = username
        user.whatsapp_number = mobile  # same as mobile
        user.password = make_password(self.cleaned_data.get("password"))

        if commit:
            user.save()
        return user
