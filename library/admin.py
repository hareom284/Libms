from django.contrib import admin
from .models import Book, UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'date_of_birth')
    search_fields = ('user__username', 'user__email', 'phone_number')
    list_filter = ('date_of_birth',)


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


# Customize admin site headers
admin.site.site_header = "Library Management System Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Management System"
