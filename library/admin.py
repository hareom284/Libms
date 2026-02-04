from django.contrib import admin
from .models import Book, UserProfile, Review


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


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')
    search_fields = ('book__title', 'user__username', 'review_text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Review Information', {
            'fields': ('book', 'user', 'rating')
        }),
        ('Review Content', {
            'fields': ('review_text',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    list_per_page = 20

    def get_queryset(self, request):
        """
        Optimize queryset with select_related to reduce database queries
        """
        qs = super().get_queryset(request)
        return qs.select_related('book', 'user')


# Customize admin site headers
admin.site.site_header = "Library Management System Administration"
admin.site.site_title = "Library Admin"
admin.site.index_title = "Welcome to Library Management System"
