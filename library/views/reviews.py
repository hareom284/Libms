"""
Review Views
Handles all review-related operations including add, edit, and delete
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Book, Review
from ..forms import ReviewForm


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
    return render(request, 'library/reviews/add_review.html', context)


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
    return render(request, 'library/reviews/edit_review.html', context)


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
    return render(request, 'library/reviews/delete_review_confirm.html', context)
