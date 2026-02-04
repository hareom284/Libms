"""
Views Package
Exports all view functions for easy importing
"""

# Book views
from .books import (
    index,
    book_list,
    book_detail,
    book_create,
    book_update,
    book_delete,
)

# Review views
from .reviews import (
    add_review,
    edit_review,
    delete_review,
)

# Authentication views
from .auth import (
    user_register,
    registration_success,
    user_login,
    user_logout,
)

# User dashboard and profile views
from .users import (
    user_dashboard,
    user_profile,
    staff_dashboard,
)

# Search views
from .search import (
    book_search,
)

__all__ = [
    # Books
    'index',
    'book_list',
    'book_detail',
    'book_create',
    'book_update',
    'book_delete',
    # Reviews
    'add_review',
    'edit_review',
    'delete_review',
    # Auth
    'user_register',
    'registration_success',
    'user_login',
    'user_logout',
    # Users
    'user_dashboard',
    'user_profile',
    'staff_dashboard',
    # Search
    'book_search',
]
