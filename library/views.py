from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Book
from .forms import BookForm


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
