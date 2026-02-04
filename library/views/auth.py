"""
Authentication Views
Handles user registration, login, logout, and related authentication operations
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from ..forms import UserRegistrationForm, UserLoginForm


def user_register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Log the user in after registration
            login(request, user)

            # Send confirmation email
            try:
                send_mail(
                    subject='Welcome to Silent Library!',
                    message=f'Hello {user.first_name},\n\nThank you for registering at Silent Library. Your account has been created successfully!\n\nUsername: {user.username}\n\nYou can now login and start exploring our collection.\n\nBest regards,\nSilent Library Team',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
            except Exception as e:
                # Log error but don't prevent registration
                print(f"Error sending email: {e}")

            messages.success(request, f'Welcome {user.first_name}! Your account has been created successfully.')
            return redirect('registration_success')
    else:
        form = UserRegistrationForm()

    context = {'form': form}
    return render(request, 'library/auth/register.html', context)


def registration_success(request):
    """Registration success page"""
    return render(request, 'library/auth/registration_success.html')


def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    context = {'form': form}
    return render(request, 'library/auth/login.html', context)


def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')
