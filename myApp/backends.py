# backends.py in your Django app

from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import Citizen

class CitizenAuthenticationBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            citizen = Citizen.objects.get(email=email)
            if check_password(password, citizen.password):
                return citizen
            else:
                return None
        except Citizen.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Citizen.objects.get(pk=user_id)
        except Citizen.DoesNotExist:
            return None
