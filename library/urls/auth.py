"""
Authentication URLs
All authentication and password reset URL patterns
"""
from django.urls import path
from django.contrib.auth import views as auth_views
from ..views import auth as auth_views_custom

urlpatterns = [
    # User Authentication
    path('register/', auth_views_custom.user_register, name='register'),
    path('registration-success/', auth_views_custom.registration_success, name='registration_success'),
    path('login/', auth_views_custom.user_login, name='login'),
    path('logout/', auth_views_custom.user_logout, name='logout'),

    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='library/auth/password_reset.html',
             email_template_name='library/auth/password_reset_email.html',
             subject_template_name='library/auth/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='library/auth/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='library/auth/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='library/auth/password_reset_complete.html'
         ),
         name='password_reset_complete'),
]
