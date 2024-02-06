from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    # Указываем, что email должен быть уникальным
    username = models.CharField(_('username'), max_length=12, unique=True)
    email = models.EmailField(_('email address'), unique=True)
    

    # Возвращаем email в качестве строкового представления объекта
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
