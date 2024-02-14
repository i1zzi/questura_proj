from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser, Citizen, Slot_Type, Appointment, Booking

# Citizen registration form, also usese a Django User auth. form, but with some modifications via CustomUser
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

# Uses basic Django ModelForm, the major info about the appointment
class SlotForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['slot_name', 'start_time', 'end_time', 'location']
        widgets = {
            'start_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),

        }
            
# Still has some issuies with double booking. Basically, 'cos of the clean metho. I developed an integreate it after tha major part,
# so i was not able to fix it in last minute, sorry 
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['slot']  # Here's the problem, you need to choose the slot again, but you've alread choose it on citizen_profile

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Take user from view
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        slot = cleaned_data.get("slot")

        # cheking if slot is NONO
        if slot is None:
            raise ValidationError("Please, choose a slot")


        # cheking if user tying to book "Collect passport"
        if slot.slot_name.name == "Collect passport":
            # cheking if user has "passport release" befor booking collect
            user_citizen = Citizen.objects.get(user=self.user)
            release_slots = Slot_Type.objects.filter(name__contains="Passport release")
            user_bookings = Booking.objects.filter(user=user_citizen, slot__slot_name__in=release_slots)
        
        # Sorting by time, so collect can bee booked only in 30+ days after release
        if slot.slot_name.name == "Collect passport":
            user_citizen = Citizen.objects.get(user=self.user)
            release_slots = Booking.objects.filter(
                user=user_citizen,
                slot__slot_name__name__contains="Passport release"
            ).order_by('-slot__start_time')
            
        # Cheking if 30+ days
            if release_slots.exists():
                last_release_date = release_slots.first().slot.start_time
                if (slot.start_time - last_release_date).days < 30:
                    raise ValidationError("Passport collection is available no earlier than 30 days after the request for release.")

            if not user_bookings.exists():
                raise ValidationError("You cannot book 'Collect passport' without having booked slots on 'Passport release'")

        return cleaned_data


