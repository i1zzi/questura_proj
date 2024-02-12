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

class Slot_Type(models.Model):
    name = models.CharField(max_length=150) # Название услуги
    description = models.TextField() #Описание услуги

    def __str__(self):
        return self.name
    
class Appointment(models.Model):
    slot_name = models.ForeignKey(Slot_Type, on_delete=models.CASCADE) #Ключ на Slot_Type с назвнаием

    # Время аппойтмента
    start_time = models.DateTimeField() 
    end_time = models.DateTimeField()

    location = models.CharField(max_length=150) # Видимо описание/адрес квестуры в которой будет аппойтмент

    #Доступность для бронирования 
    # я тебя молю, не забывай что ты написала is_avaliable с ошибкой
    is_avaliable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.slot_name.name} at {self.start_time} - {self.end_time}"
    
class Booking(models.Model):
    user = models.ForeignKey(Citizen, on_delete=models.CASCADE)  # Ссылка на пользователя
    slot = models.ForeignKey(Appointment, on_delete=models.CASCADE)  # Ссылка на аппойтмент, который букается
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания бронирования

    def __str__(self):
        return f"{self.user.email} booked {self.slot}"