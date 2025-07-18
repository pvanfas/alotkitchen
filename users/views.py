# Create your views here.
from django.shortcuts import render, redirect
from .forms import UserForm
from django.contrib.auth import login

def custom_register(request):
    try:
        if request.method == 'POST':
            form = UserForm(request.POST)
            if form.is_valid():
                user = form.save()  
                login(request, user)  
                return redirect('main:home_view')  # or some success page
        else:
            form = UserForm()
        return render(request, 'registration/registration_form.html', {'form': form})
    except Exception as e:
        print(f"Error in custom_register: {e}")
        # Return an error response instead of None
        return render(request, 'registration/registration_form.html', {
            'form': UserForm(),
            'error': 'An error occurred during registration. Please try again.'
        })
