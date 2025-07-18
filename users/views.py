# Create your views here.
from django.contrib.auth import login
from django.shortcuts import redirect, render

from .forms import UserForm


def custom_register(request):
    try:
        if request.method == "POST":
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()
                login(request, user)
                return redirect("main:dashboard_view")
        else:
            form = UserForm()
        return render(request, "registration/registration_form.html", {"form": form})
    except Exception as e:
        print(f"Error in custom_register: {e}")
        # Return an error response instead of None
        return render(request, "registration/registration_form.html", {"form": UserForm(), "error": "An error occurred during registration. Please try again."})
