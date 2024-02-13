from django.shortcuts import get_object_or_404, render, redirect
#from django.contrib.auth.views import LoginView
from django.contrib import messages
from .forms import CitizenRegistrationForm, SlotForm, BookingForm
from django.contrib.auth import authenticate, login
from .models import CustomUser, Slot_Type, Appointment, Booking
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

# Иморт для букинда аппойтментов
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse_lazy


# Формы, отвечающие за регистрацию и вход пользователя
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
    # Получаем текущего пользователя
    user = request.user
    # Предполагаем, что у пользователя есть связь с моделью Citizen через OneToOneField
    # и что модель Booking связана с Citizen
    citizen = user.citizen
    # Получаем все забронированные слоты для текущего пользователя
    booked_slots = Booking.objects.filter(user=citizen)
    # Получаем все доступные для бронирования слоты
    avaliable_slots = Appointment.objects.filter(is_avaliable=True)
    
    # Передаем забронированные и доступные слоты в шаблон
    context = {
        'booked_slots': booked_slots,
        'avaliable_slots': avaliable_slots,
    }
    return render(request, 'citizen_profile.html', context)

# Начальная страница для ментов
def manage_slots(request):
    return render(request, 'manage_slots.html') # тут пока не понятно, нужна ли эта форма

#создание нового свободного слота ментом
class SlotCreateView(CreateView):
    model = Appointment
    form_class = SlotForm
    template_name = 'slot_create.html' # пока нет тэмплэйта
    success_url = reverse_lazy('slot_list')  # пока нет URL с именем 'slot_list'

#просмотр всех созданных слотов ментами
class SlotListView(ListView):
    model = Appointment
    context_object_name = 'slot_list'
    template_name = 'slot_list.html'

#в теории, редакирование слота, но хуй оно мне надо, если эёот можно делать через Django admin
class SlotUpdateView(UpdateView):
    model = Appointment
    form_class = SlotForm
    template_name = 'slots/slot_form.html'
    success_url = reverse_lazy('slot_list')

#вот это букинг аппойтмента со свтороны пользователя, помни о том, как написано is_avaliable
#вот тут начали менять 
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
            slot.is_avaliable = False  # Обновляем статус слота
            slot.save()
            messages.success(request, f'Booking for {slot.slot_name.name} from {slot.start_time} to {slot.end_time} in {slot.location} was successful. Do not forget downlisted documents:   ')
            return redirect('citizen_profile') # пофиксили, все ок
    else:
        form = BookingForm(user=request.user)
    return render(request, 'book_slot.html', {'form': form, 'slot': slot})
