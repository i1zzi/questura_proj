# #from django.db import models
# #from django.contrib.auth.models import AbstractUser
# #from django.contrib.auth.forms import UserCreationForm
# #from .models import CustomUser
# ##from django import forms

# #class CustomUserCreationForm(UserCreationForm):
# #    email = forms.EmailField(required=True, help_text='Required. Add a valid email address.')

#     class Meta(UserCreationForm.Meta):
#         model = CustomUser
#         fields = ('email', 'password1', 'password2')  # Используем email вместо username

#     def __init__(self, *args, **kwargs):
#         super(CustomUserCreationForm, self).__init__(*args, **kwargs)
#         if 'username' in self.fields:
#             del self.fields['username']  # Удаляем поле username, если оно есть

# class Citizen(models.Model):
#     # user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=120)
#     date_of_birth = models.DateField()
#     place_of_birth =models.CharField(max_length=110)
#     tax_code = models.CharField(max_length=16, unique=True)
#     email = models.EmailField()

#     def __str__(self):
#         return f"{self.first_name} {self.last_name}"

from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    # Если вы хотите убрать username, добавьте следующие строки:
    username = None
    email = models.EmailField('Email address', unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Citizen(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    place_of_birth = models.CharField(max_length=110)
    tax_code = models.CharField(max_length=16, unique=True)
    email = models.EmailField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
