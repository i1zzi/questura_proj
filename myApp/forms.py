from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Citizen, Slot_Type, Appointment, Booking

class CitizenRegistrationForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = Citizen
        fields = ('first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'tax_code')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def save(self, commit=True):
        user = CustomUser.objects.create_user(
            username=self.cleaned_data['email'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        citizen = super(CitizenRegistrationForm, self).save(commit=False)
        citizen.user = user
        if commit:
            citizen.save()
            return citizen

class SlotForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['slot_name', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }
            
# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = []  # Все данные определяются в представлении    


## так последняя запись, вообще, оно работает, и даже показывает сообщение о том, что нельзя забронировать.
        #но, проблема в том, что теперь он показывает все слоты(даже не активные, которые были забронированы другим пользователем)
        #и до кучи все равно бронирует Collect Passport, после сообщения о том, что его нельзя забронировать.
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot']  # Поле выбора слота для бронирования

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Принимаем пользователя из представления
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        slot = cleaned_data.get("slot")

        # Добавляем проверку на None для объекта slot
        if slot is None:
            raise ValidationError("Необходимо выбрать слот для бронирования.")


        # Проверка, что пользователь пытается забронировать "Collect passport"
        if slot.slot_name.name == "Collect passport":
            # Проверяем, есть ли у пользователя забронированные слоты на выпуск паспорта
            user_citizen = Citizen.objects.get(user=self.user)
            release_slots = Slot_Type.objects.filter(name__contains="Passport release")
            user_bookings = Booking.objects.filter(user=user_citizen, slot__slot_name__in=release_slots)
        
        # Тут сортируем по времени слоты у пользователя
        if slot.slot_name.name == "Collect passport":
            user_citizen = Citizen.objects.get(user=self.user)
            release_slots = Booking.objects.filter(
                user=user_citizen,
                slot__slot_name__name__contains="Passport release"
            ).order_by('-slot__start_time')
            
        # Проверяем, пооршло ли больше 30 дней с моменты подачи
            if release_slots.exists():
                last_release_date = release_slots.first().slot.start_time
                if (slot.start_time - last_release_date).days < 30:
                    raise ValidationError("Сбор паспорта доступен не ранее чем через 30 дней после запроса на выпуск.")

            if not user_bookings.exists():
                raise ValidationError("Вы не можете забронировать 'Collect passport', не имея забронированных слотов на 'Passport release'")

        return cleaned_data

# на потом
# class BookingForm(forms.ModelForm):
#     class Meta:
#         model = Booking
#         fields = ['slot']  # Пользователь выбирает слот при бронировании

#     def clean(self):
#         cleaned_data = super().clean()
#         slot = cleaned_data.get('slot')
        
#         # Проверка на конкретные условия зависимости
#         if slot and slot.slot_name.name == "Collect passport":
#             # Проверяем, есть ли у пользователя необходимые бронирования
#             # Это может потребовать выполнения запросов к базе данных
#             # Например, проверить, есть ли у текущего пользователя бронирование типа "Passport release"
#             has_required_booking = ...  # Здесь должна быть ваша логика проверки

#             if not has_required_booking:
#                 # Если условие не удовлетворено, добавляем ошибку к форме
#                 self.add_error('slot', "Сначала необходимо забронировать слот 'Passport release'.")

#         return cleaned_data

