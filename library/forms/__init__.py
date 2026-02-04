"""
Forms Package
Exports all form classes for easy importing
"""
from .auth import UserRegistrationForm, UserLoginForm
from .user import UserProfileForm, UserUpdateForm
from .book import BookForm
from .review import ReviewForm

__all__ = [
    'UserRegistrationForm',
    'UserLoginForm',
    'UserProfileForm',
    'UserUpdateForm',
    'BookForm',
    'ReviewForm',
]
