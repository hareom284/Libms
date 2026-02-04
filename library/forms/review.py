"""
Review Forms
Forms for book reviews and ratings
"""
from django import forms
from ..models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for users to submit book reviews and ratings
    """
    class Meta:
        model = Review
        fields = ['rating', 'review_text']
        widgets = {
            'rating': forms.Select(attrs={
                'class': 'form-select',
                'required': True
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Share your thoughts about this book...'
            })
        }
        labels = {
            'rating': 'Your Rating',
            'review_text': 'Your Review (Optional)'
        }
