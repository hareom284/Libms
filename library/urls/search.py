"""
Search URLs
Book search URL patterns
"""
from django.urls import path
from ..views import search

urlpatterns = [
    # Book Search
    path('search/', search.book_search, name='book_search'),
]
