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
