"""
Review URLs
All review-related URL patterns
"""
from django.urls import path
from ..views import reviews

urlpatterns = [
    # Review operations
    path('books/<int:book_id>/review/add/', reviews.add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', reviews.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', reviews.delete_review, name='delete_review'),
]
