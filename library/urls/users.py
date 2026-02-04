"""
User URLs
User dashboard, profile, and staff dashboard URL patterns
"""
from django.urls import path
from ..views import users

urlpatterns = [
    # User Dashboard & Profile
    path('dashboard/', users.user_dashboard, name='user_dashboard'),
    path('profile/', users.user_profile, name='user_profile'),

    # Staff Dashboard
    path('staff/dashboard/', users.staff_dashboard, name='staff_dashboard'),
]
