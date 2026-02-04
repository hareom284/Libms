"""
Admin Package
Imports all admin configurations and customizes Django admin site
"""
from django.contrib import admin
from .user import UserProfileAdmin
from .book import BookAdmin
from .review import ReviewAdmin

# Customize admin site headers
admin.site.site_header = "Library Management System Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Management System"

__all__ = [
    'UserProfileAdmin',
    'BookAdmin',
    'ReviewAdmin',
]
