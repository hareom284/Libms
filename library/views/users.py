"""
User Dashboard and Profile Views
Handles user dashboard, profile management, and staff dashboard
"""
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from ..models import Book, UserProfile, Review
from ..forms import UserProfileForm, UserUpdateForm


@login_required
def user_dashboard(request):
    """User personalized dashboard"""
    context = {
        'user': request.user,
    }
    return render(request, 'library/users/dashboard.html', context)


@login_required
def user_profile(request):
    """View and edit user profile"""
    # Ensure user has a profile - create one if it doesn't exist
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('user_profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'library/users/profile.html', context)


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
    return render(request, 'library/users/staff_dashboard.html', context)
