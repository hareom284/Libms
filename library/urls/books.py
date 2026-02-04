"""
Book URLs
All book-related URL patterns including home page
"""
from django.urls import path
from ..views import books

urlpatterns = [
    # Home page
    path('', books.index, name='index'),

    # Book CRUD operations
    path('books/', books.book_list, name='book_list'),
    path('books/create/', books.book_create, name='book_create'),
    path('books/<int:pk>/', books.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', books.book_update, name='book_update'),
    path('books/<int:pk>/delete/', books.book_delete, name='book_delete'),
]
