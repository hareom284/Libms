"""
URLs Package
Combines all URL patterns from different modules
"""
from django.urls import path, include
from . import books, reviews, auth, users, search

# Combine all URL patterns
urlpatterns = []

# Add patterns from each module
urlpatterns += books.urlpatterns
urlpatterns += reviews.urlpatterns
urlpatterns += auth.urlpatterns
urlpatterns += users.urlpatterns
urlpatterns += search.urlpatterns
