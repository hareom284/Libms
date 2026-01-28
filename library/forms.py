from django import forms
from .models import Book


class BookForm(forms.ModelForm):
    """
    Form for creating and updating Book instances
    """
    class Meta:
        model = Book
        fields = ['title', 'author', 'cover_pic', 'isbn', 'description', 'category', 'published_date', 'available_copies']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter book title'
            }),
            'author': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter author name'
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter 13-digit ISBN'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Enter book description'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter category (e.g., Fiction, Non-fiction)'
            }),
            'published_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'available_copies': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0'
            }),
            'cover_pic': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
