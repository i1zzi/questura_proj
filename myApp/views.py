from django.shortcuts import render, redirect
#from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CitizenRegistrationForm
from django.contrib.auth import authenticate, login
from .models import CustomUser


# Create your views here.
def home(request):
    return render(request, 'home.html')

def citizen_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('citizen_profile')
        else:
            messages.error(request, 'Invalid login credentials. Please try again.')
    return render(request, 'citizen_login.html')

def citizen_register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('citizen_login')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'citizen_register.html', {'form': form})

def manage_slots(request):
    return render(request, 'manage_slots.html')


#class CitizenLoginView(LoginView):
    #template_name = 'citizen_login.html'


def citizen_profile(request):
    # Logic to display the citizen's profile
    return render(request, 'citizen_profile.html')