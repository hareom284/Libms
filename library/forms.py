from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from .models import Book, UserProfile, Review


class UserRegistrationForm(UserCreationForm):
    """
    Form for user registration with additional fields
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email'
        })
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your first name'
        })
    )
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your last name'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            })
        }

    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm password'
        })

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email address is already registered.')
        return email


class UserLoginForm(AuthenticationForm):
    """
    Custom login form with Bootstrap styling
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password'
        })
    )


class UserProfileForm(forms.ModelForm):
    """
    Form for editing user profile information
    """
    class Meta:
        model = UserProfile
        fields = ['phone_number', 'address', 'date_of_birth', 'profile_picture']
        widgets = {
            'phone_number': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your address'
            }),
            'date_of_birth': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'profile_picture': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }


class UserUpdateForm(forms.ModelForm):
    """
    Form for updating user account information
    """
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control'
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            })
        }


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
