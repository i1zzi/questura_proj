# from django import forms
# from django.contrib.auth.forms import UserCreationForm

# # Вход для админа в Django admin pannel
# class CustomUserCreationForm(UserCreationForm):
    
#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('username', 'email', 'password1')

# class CitizenRegistrationForm(forms.ModelForm):
#     email = forms.EmailField(required=True)
#     password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
#     password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

#     class Meta:
#         model = Citizen
#         fields = ('first_name', 'last_name', 'date_of_birth', 'place_of_birth', 'tax_code')
#         widgets = {
#             'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
#         }
    
#     def save(self, commit=True):
#         user = CustomUser.objects.create_user(
#             username=self.cleaned_data['email'],
#             email=self.cleaned_data['email'],
#             password=self.cleaned_data['password1']
#         )
#         citizen = super(CitizenRegistrationForm, self).save(commit=False)
#         citizen.user = user
#         if commit:
#             citizen.save()
#             return citizen
        
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Citizen


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            del self.fields['username']

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