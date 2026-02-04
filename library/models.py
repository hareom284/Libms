from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    Extended user profile model to store additional user information
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=15, blank=True, null=True, help_text="Enter phone number")
    address = models.TextField(blank=True, null=True, help_text="Enter address")
    date_of_birth = models.DateField(blank=True, null=True, help_text="Enter date of birth")
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True, help_text="Upload profile picture")

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.username}'s Profile"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create UserProfile when a new User is created
    """
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """
    Save UserProfile when User is saved
    """
    if hasattr(instance, 'profile'):
        instance.profile.save()


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
