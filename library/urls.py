from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Home page
    path('', views.index, name='index'),

    # Book CRUD operations
    path('books/', views.book_list, name='book_list'),
    path('books/create/', views.book_create, name='book_create'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/edit/', views.book_update, name='book_update'),
    path('books/<int:pk>/delete/', views.book_delete, name='book_delete'),

    # User Authentication
    path('register/', views.user_register, name='register'),
    path('registration-success/', views.registration_success, name='registration_success'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),

    # User Dashboard & Profile
    path('dashboard/', views.user_dashboard, name='user_dashboard'),
    path('profile/', views.user_profile, name='user_profile'),

    # Password Reset
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='library/password_reset.html',
             email_template_name='library/password_reset_email.html',
             subject_template_name='library/password_reset_subject.txt'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='library/password_reset_done.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='library/password_reset_confirm.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='library/password_reset_complete.html'
         ),
         name='password_reset_complete'),

    # Book Search
    path('search/', views.book_search, name='book_search'),

    # Review URLs
    path('books/<int:book_id>/review/add/', views.add_review, name='add_review'),
    path('reviews/<int:review_id>/edit/', views.edit_review, name='edit_review'),
    path('reviews/<int:review_id>/delete/', views.delete_review, name='delete_review'),

    # Staff Dashboard
    path('staff/dashboard/', views.staff_dashboard, name='staff_dashboard'),
]
