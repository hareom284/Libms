"""
Book CRUD Views
Handles all book-related operations including list, detail, create, update, and delete
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from ..models import Book
from ..forms import BookForm


def index(request):
    """Home page view"""
    # Get recently added books (limit to 8 for home page display)
    recent_books = Book.objects.all().order_by('-id')[:8]

    # Get statistics
    total_books = Book.objects.count()
    total_categories = Book.objects.values('category').distinct().count()
    total_authors = Book.objects.values('author').distinct().count()
    available_books = Book.objects.filter(available_copies__gt=0).count()

    context = {
        'recent_books': recent_books,
        'total_books': total_books,
        'total_categories': total_categories,
        'total_authors': total_authors,
        'available_books': available_books,
    }
    return render(request, 'library/index.html', context)


def book_list(request):
    """Display list of all books"""
    books = Book.objects.all().order_by('title')
    context = {
        'books': books
    }
    return render(request, 'library/books/book_list.html', context)


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
    return render(request, 'library/books/book_detail.html', context)


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
    return render(request, 'library/books/book_form.html', context)


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
    return render(request, 'library/books/book_form.html', context)


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
    return render(request, 'library/books/book_confirm_delete.html', context)
