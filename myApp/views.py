from django.shortcuts import get_object_or_404, render, redirect
#from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CitizenRegistrationForm, SlotForm, BookingForm
from django.contrib.auth import authenticate, login
from .models import CustomUser, Slot_Type, Appointment, Booking
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# for appointment's booking
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy

# CITIZEN FORMS
# home, registration and login forms
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
            messages.error(request, 'Invalid Login. Please try again or contact us at police@govn.it (You shall consider sending us a pigeon, it might be faster than an email.)')
    return render(request, 'citizen_login.html')

def citizen_register(request):
    if request.method == 'POST':
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('citizen_profile')
    else:
        form = CitizenRegistrationForm()
    return render(request, 'citizen_register.html', {'form': form})

#class CitizenLoginView(LoginView):
    #template_name = 'citizen_login.html'

#  тут часть, которая нормальноработала, до того пока  я не начала пытаться показывать заброненые пользователем аппойтменты
# def citizen_profile(request):
#     avaliable_slots = Appointment.objects.filter(is_avaliable=True)
#     print(avaliable_slots)  # Для отладки
#     return render(request, 'citizen_profile.html', {'avaliable_slots': avaliable_slots})

# тут то же, но с попыткой показывать заброненые слоты, и оно даже работает
@login_required
def citizen_profile(request):
    # getting the user
    user = request.user
    # Assume that the user has a connection to the Citizen model via OneToOneField
     # and that the Booking model is related to Citizen
    citizen = user.citizen
    # Get all reserved slots for the current user
    booked_slots = Booking.objects.filter(user=citizen)
    # get all slots available for booking
    avaliable_slots = Appointment.objects.filter(is_avaliable=True)
    
    # Pass reserved and available slots to the template
    context = {
        'booked_slots': booked_slots,
        'avaliable_slots': avaliable_slots,
    }
    return render(request, 'citizen_profile.html', context)

#POLICE FORMS
# police stuff home-page
def manage_slots(request):
    return render(request, 'manage_slots.html') # тут пока не понятно, нужна ли эта форма

#create a new slot by police
class SlotCreateView(CreateView):
    model = Appointment
    form_class = SlotForm
    template_name = 'slot_create.html' # пока нет тэмплэйта
    success_url = reverse_lazy('slot_list')  # пока нет URL с именем 'slot_list'

#view all the slots by police
class SlotListView(ListView):
    model = Appointment
    context_object_name = 'slot_list'
    template_name = 'slot_list.html'

#в теории, редакирование слота, но зачем оно мне надо, если это можно делать через Django admin
class SlotUpdateView(UpdateView):
    model = Appointment
    form_class = SlotForm
    template_name = 'slots/slot_form.html'
    success_url = reverse_lazy('slot_list')

##this is the booking of the application from the user’s side, remember how "is_avaliable" is written
    
@login_required
def book_slot(request, slot_id):
    slot = get_object_or_404(Appointment, pk=slot_id, is_avaliable=True)
    if request.method == 'POST':
        form = BookingForm(request.POST, user=request.user)
        if form.is_valid():
            booking = form.save(commit=False)
            citizen_user = request.user.citizen
            booking.user = citizen_user
            booking.slot = slot
            booking.save()
            slot.is_avaliable = False  # updatin the status
            slot.save()
            messages.success(request, f'Booking for {slot.slot_name.name} from {slot.start_time} to {slot.end_time} in {slot.location} was successful. Do not forget downlisted documents:   ')
            return redirect('citizen_profile') 
    else:
        form = BookingForm(user=request.user)
    return render(request, 'book_slot.html', {'form': form, 'slot': slot})
