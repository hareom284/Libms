"""
Book Model
Represents a book in the library management system
"""
from django.db import models


class Book(models.Model):
    """
    Model representing a book in the library management system.
    """
    title = models.CharField(max_length=200, help_text="Enter the book title")
    author = models.CharField(max_length=200, help_text="Enter the author's name")
    cover_pic = models.ImageField(
        upload_to='cover_pics/',
        blank=True,
        null=True,
        help_text="Upload book cover image"
    )
    isbn = models.CharField(
        max_length=13,
        unique=True,
        help_text="Enter 13-character ISBN number"
    )
    description = models.TextField(help_text="Enter a detailed description of the book")
    category = models.CharField(max_length=50, help_text="Enter the book's category")
    published_date = models.DateField(help_text="Enter the publication date")
    available_copies = models.IntegerField(
        default=1,
        help_text="Number of available copies"
    )

    class Meta:
        ordering = ['title']
        verbose_name = 'Book'
        verbose_name_plural = 'Books'

    def __str__(self):
        """
        String representation of the Book object.
        Returns the book's title and ISBN number.
        """
        return f"{self.title} (ISBN: {self.isbn})"

    def get_average_rating(self):
        """
        Calculate and return the average rating for this book
        """
        reviews = self.reviews.all()
        if reviews:
            total = sum(review.rating for review in reviews)
            return round(total / len(reviews), 1)
        return 0

    def get_review_count(self):
        """
        Return the total number of reviews for this book
        """
        return self.reviews.count()
