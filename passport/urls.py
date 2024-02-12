"""
URL configuration for passport project.
"""
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from myApp.views import home, citizen_login, citizen_register, citizen_profile, manage_slots, SlotUpdateView, SlotCreateView, SlotListView, book_slot


urlpatterns = [
    path('admin/', admin.site.urls),
    path('staff-login/', auth_views.LoginView.as_view(template_name='staff_login.html'), name='staff-login'),
    path('', home, name='home'), # PD Home URL
    path('manage-slots/', manage_slots, name='manage-slots'),
    path('citizen-login/', citizen_login, name='citizen_login'),
    path('citizen-register/', citizen_register, name='citizen_register'),
    path('citizen/profile/', citizen_profile, name='citizen_profile'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('slots/new', SlotCreateView.as_view(), name='slot_create'),
    path('slots/list', SlotListView.as_view(), name='slot_list'),
    path('slots/<int:pk>/edit/', SlotUpdateView.as_view(), name='slot_edit'),
    path('slots/<int:slot_id>/book/', book_slot, name='book_slot'),
]
