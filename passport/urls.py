"""
URL configuration for passport project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myApp.views import home, citizen_login, citizen_register, citizen_profile, manage_slots


urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff-login/', auth_views.LoginView.as_view(template_name='staff_login.html'), name='staff-login'),
    path('', home, name='home'), # PD Home URL
    path('manage-slots/', manage_slots, name='manage-slots'),
    path('citizen-login/', citizen_login, name='citizen_login'),
    path('citizen-register/', citizen_register, name='citizen_register'),
    path('citizen/profile/', citizen_profile, name='citizen_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
