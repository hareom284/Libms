"""
Review Admin
Django admin configuration for Review model
"""
from django.contrib import admin
from ..models import Review


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
