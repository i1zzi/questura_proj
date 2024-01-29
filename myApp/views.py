from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import CustomUserCreationForm
from .models import Profile

# Create your views here.
def home(request):
    return render(request, 'home.html')

def manage_slots(request):
    return render(request, 'manage_slots.html')

def citizen(request):
    return render(request, 'citizen.html')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create Profile instance
            profile = Profile(user=user, tax_code=form.cleaned_data['tax_code'], 
                              date_of_birth=form.cleaned_data['date_of_birth'],
                              place_of_birth=form.cleaned_data['place_of_birth'])
            profile.save()
            # Redirect or show success message
            return redirect('login')  # Redirect to a login or success page
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

class CitizenLoginView(LoginView):
    template_name = 'citizen_login.html' 