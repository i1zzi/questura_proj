from django import forms
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
            
class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = []  # Все данные определяются в представлении        
