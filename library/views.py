from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Book, UserProfile
from .forms import (
    BookForm, UserRegistrationForm, UserLoginForm,
    UserProfileForm, UserUpdateForm
)


def index(request):
    """Home page view"""
    return render(request, 'library/index.html')


def book_list(request):
    """Display list of all books"""
    books = Book.objects.all().order_by('title')
    context = {
        'books': books
    }
    return render(request, 'library/book_list.html', context)


def book_detail(request, pk):
    """Display details of a single book"""
    book = get_object_or_404(Book, pk=pk)
    context = {
        'book': book
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def book_create(request):
    """Create a new book"""
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" was created successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm()

    context = {
        'form': form,
        'title': 'Add New Book'
    }
    return render(request, 'library/book_form.html', context)


@login_required
def book_update(request, pk):
    """Update an existing book"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save()
            messages.success(request, f'Book "{book.title}" was updated successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = BookForm(instance=book)

    context = {
        'form': form,
        'book': book,
        'title': f'Edit: {book.title}'
    }
    return render(request, 'library/book_form.html', context)


@login_required
def book_delete(request, pk):
    """Delete a book"""
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book_title = book.title
        book.delete()
        messages.success(request, f'Book "{book_title}" was deleted successfully!')
        return redirect('book_list')

    context = {
        'book': book
    }
    return render(request, 'library/book_confirm_delete.html', context)


# ============= User Authentication Views =============

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
    return render(request, 'library/register.html', context)


def registration_success(request):
    """Registration success page"""
    return render(request, 'library/registration_success.html')


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
    return render(request, 'library/login.html', context)


@login_required
def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('index')


@login_required
def user_dashboard(request):
    """User personalized dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'library/dashboard.html', context)


@login_required
def user_profile(request):
    """View and edit user profile"""
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'library/profile.html', context)


# ============= Search Views =============

def book_search(request):
    """Search books by title, author, or genre"""
    query = request.GET.get('q', '')
    search_type = request.GET.get('type', 'all')

    books = Book.objects.all()

    if query:
        if search_type == 'title':
            books = books.filter(title__icontains=query)
        elif search_type == 'author':
            books = books.filter(author__icontains=query)
        elif search_type == 'genre':
            books = books.filter(category__icontains=query)
        else:  # 'all' - search in all fields
            books = books.filter(
                Q(title__icontains=query) |
                Q(author__icontains=query) |
                Q(category__icontains=query) |
                Q(description__icontains=query)
            )

    context = {
        'books': books,
        'query': query,
        'search_type': search_type
    }
    return render(request, 'library/search_results.html', context)
