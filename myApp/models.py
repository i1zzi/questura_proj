from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Citizen(models.Model):
    firstName = models.CharField(max_length=100)
    lastName = models.CharField(max_length=120)
    dateOfBirth = models.DateField()
    placeOfBirth =models.CharField(max_length=110)
    taxCode = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.firstName} {self.lastName}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    taxCode = models.CharField(max_length=16, unique=True)
    dateOfBirth =models.DateField()
    placeOfBirth = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username
