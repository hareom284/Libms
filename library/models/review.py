"""
Review Model
Represents user reviews and ratings for books
"""
from django.db import models
from django.contrib.auth.models import User
from .book import Book


class Review(models.Model):
    """
    Model representing a user review for a book.
    Allows registered users to rate and review books.
    """
    RATING_CHOICES = [
        (1, '1 - Poor'),
        (2, '2 - Fair'),
        (3, '3 - Good'),
        (4, '4 - Very Good'),
        (5, '5 - Excellent'),
    ]

    book = models.ForeignKey(
        Book,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="Book being reviewed"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text="User who wrote the review"
    )

    rating = models.IntegerField(
        choices=RATING_CHOICES,
        help_text="Rating from 1 to 5 stars"
    )

    review_text = models.TextField(
        help_text="Detailed review of the book",
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Book Review'
        verbose_name_plural = 'Book Reviews'
        ordering = ['-created_at']
        # Ensure one review per user per book
        unique_together = ['book', 'user']

    def __str__(self):
        return f"{self.user.username}'s review of {self.book.title} - {self.rating} stars"

    def get_star_display(self):
        """
        Return star rating as string (e.g., '★★★★☆')
        """
        filled_stars = '★' * self.rating
        empty_stars = '☆' * (5 - self.rating)
        return filled_stars + empty_stars
