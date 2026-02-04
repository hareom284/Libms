from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from .models import Book, UserProfile, Review
from .forms import (
    BookForm, UserRegistrationForm, UserLoginForm,
    UserProfileForm, UserUpdateForm, ReviewForm
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
    """Display details of a single book with reviews"""
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.all().select_related('user')

    # Check if current user has already reviewed this book
    user_review = None
    if request.user.is_authenticated:
        user_review = reviews.filter(user=request.user).first()

    context = {
        'book': book,
        'reviews': reviews,
        'user_review': user_review,
        'average_rating': book.get_average_rating(),
        'review_count': book.get_review_count()
    }
    return render(request, 'library/book_detail.html', context)


@login_required
def book_create(request):
    """Create a new book - Staff only"""
    # Check if user is staff
    if not request.user.is_staff:
        messages.error(request, 'Only library staff can add books.')
        return redirect('book_list')

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
    """Update an existing book - Staff only"""
    # Check if user is staff
    if not request.user.is_staff:
        messages.error(request, 'Only library staff can edit books.')
        return redirect('book_detail', pk=pk)

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
    """Delete a book - Staff only"""
    # Check if user is staff
    if not request.user.is_staff:
        messages.error(request, 'Only library staff can delete books.')
        return redirect('book_detail', pk=pk)

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


# ============= Review Views =============

@login_required
def add_review(request, book_id):
    """
    Allow authenticated users to add a review for a book
    """
    book = get_object_or_404(Book, pk=book_id)

    # Check if user has already reviewed this book
    existing_review = Review.objects.filter(book=book, user=request.user).first()

    if existing_review:
        messages.warning(request, 'You have already reviewed this book. You can edit your existing review.')
        return redirect('edit_review', review_id=existing_review.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect('book_detail', pk=book.pk)
    else:
        form = ReviewForm()

    context = {
        'form': form,
        'book': book
    }
    return render(request, 'library/add_review.html', context)


@login_required
def edit_review(request, review_id):
    """
    Allow users to edit their own reviews
    """
    review = get_object_or_404(Review, pk=review_id)

    # Ensure user can only edit their own reviews
    if review.user != request.user:
        messages.error(request, 'You can only edit your own reviews.')
        return redirect('book_detail', pk=review.book.pk)

    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your review has been updated successfully!')
            return redirect('book_detail', pk=review.book.pk)
    else:
        form = ReviewForm(instance=review)

    context = {
        'form': form,
        'review': review,
        'book': review.book
    }
    return render(request, 'library/edit_review.html', context)


@login_required
def delete_review(request, review_id):
    """
    Allow users to delete their own reviews
    Staff can delete any review (moderation)
    """
    review = get_object_or_404(Review, pk=review_id)

    # Check permissions: user owns review OR user is staff
    if review.user != request.user and not request.user.is_staff:
        messages.error(request, 'You can only delete your own reviews.')
        return redirect('book_detail', pk=review.book.pk)

    if request.method == 'POST':
        book_pk = review.book.pk
        review_author = review.user.username
        review.delete()

        # Different message for staff moderation
        if request.user.is_staff and review.user != request.user:
            messages.success(request, f'Review by {review_author} has been deleted (staff action).')
        else:
            messages.success(request, 'Your review has been deleted successfully!')

        return redirect('book_detail', pk=book_pk)

    context = {
        'review': review,
        'book': review.book
    }
    return render(request, 'library/delete_review_confirm.html', context)


# ============= Staff Dashboard View =============

@login_required
def staff_dashboard(request):
    """
    Dashboard for library staff to view statistics and manage content
    Requires staff status
    """
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to access the staff dashboard.')
        return redirect('user_dashboard')

    # Get statistics
    total_books = Book.objects.count()
    total_users = UserProfile.objects.count()
    total_reviews = Review.objects.count()

    # Get recent reviews
    recent_reviews = Review.objects.all().select_related('book', 'user').order_by('-created_at')[:10]

    # Get top-rated books
    from django.db.models import Avg
    top_rated_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating')
    ).filter(avg_rating__isnull=False).order_by('-avg_rating')[:5]

    context = {
        'total_books': total_books,
        'total_users': total_users,
        'total_reviews': total_reviews,
        'recent_reviews': recent_reviews,
        'top_rated_books': top_rated_books
    }
    return render(request, 'library/staff_dashboard.html', context)
