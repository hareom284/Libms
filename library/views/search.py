"""
Search Views
Handles book search functionality
"""
from django.shortcuts import render
from django.db.models import Q
from ..models import Book


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
    return render(request, 'library/search/search_results.html', context)
