"""
Book Admin
Django admin configuration for Book model
"""
from django.contrib import admin
from ..models import Book


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'isbn', 'category', 'published_date', 'available_copies')
    list_filter = ('category', 'published_date')
    search_fields = ('title', 'author', 'isbn')
    ordering = ('title',)
    fieldsets = (
        ('Book Information', {
            'fields': ('title', 'author', 'isbn', 'category')
        }),
        ('Details', {
            'fields': ('description', 'published_date', 'available_copies')
        }),
        ('Media', {
            'fields': ('cover_pic',)
        }),
    )
    list_per_page = 10
