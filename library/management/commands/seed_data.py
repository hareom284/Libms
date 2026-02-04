"""
Management command to seed the database with sample data
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from library.models import Book, Review, UserProfile
from datetime import date, datetime
from django.utils import timezone


class Command(BaseCommand):
    help = 'Seeds the database with sample data for testing and development'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting database seeding...'))

        # Clear existing data (optional - comment out if you want to keep existing data)
        self.stdout.write('Clearing existing data...')
        Review.objects.all().delete()
        Book.objects.all().delete()
        User.objects.filter(is_superuser=False).delete()

        # Create Users
        self.stdout.write('Creating users...')
        users = self.create_users()

        # Create Books
        self.stdout.write('Creating books...')
        books = self.create_books()

        # Create Reviews
        self.stdout.write('Creating reviews...')
        self.create_reviews(users, books)

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
        self.stdout.write(self.style.SUCCESS(f'Created {len(users)} users, {len(books)} books, and multiple reviews'))
        self.stdout.write(self.style.WARNING('\nDefault Credentials:'))
        self.stdout.write('  Admin: admin / admin123')
        self.stdout.write('  Staff: staff / staff123')
        self.stdout.write('  User1: john_doe / user123')
        self.stdout.write('  User2: jane_smith / user123')

    def create_users(self):
        """Create sample users with different roles"""
        users = {}

        # Create Admin User
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@libms.com',
                password='admin123',
                first_name='Admin',
                last_name='User'
            )
            users['admin'] = admin
            self.stdout.write(self.style.SUCCESS('  ✓ Created admin user'))

        # Create Staff User
        if not User.objects.filter(username='staff').exists():
            staff = User.objects.create_user(
                username='staff',
                email='staff@libms.com',
                password='staff123',
                first_name='Staff',
                last_name='Member',
                is_staff=True
            )
            users['staff'] = staff
            self.stdout.write(self.style.SUCCESS('  ✓ Created staff user'))

        # Create Regular Users
        regular_users_data = [
            {
                'username': 'john_doe',
                'email': 'john@example.com',
                'password': 'user123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '555-0101',
                'address': '123 Main St, City, State 12345',
                'dob': date(1990, 5, 15)
            },
            {
                'username': 'jane_smith',
                'email': 'jane@example.com',
                'password': 'user123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '555-0102',
                'address': '456 Oak Ave, City, State 12345',
                'dob': date(1985, 8, 22)
            },
            {
                'username': 'bob_wilson',
                'email': 'bob@example.com',
                'password': 'user123',
                'first_name': 'Bob',
                'last_name': 'Wilson',
                'phone': '555-0103',
                'address': '789 Pine Rd, City, State 12345',
                'dob': date(1992, 3, 10)
            }
        ]

        for user_data in regular_users_data:
            if not User.objects.filter(username=user_data['username']).exists():
                user = User.objects.create_user(
                    username=user_data['username'],
                    email=user_data['email'],
                    password=user_data['password'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name']
                )

                # Update profile
                profile = user.profile
                profile.phone_number = user_data['phone']
                profile.address = user_data['address']
                profile.date_of_birth = user_data['dob']
                profile.save()

                users[user_data['username']] = user
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created user: {user_data["username"]}'))

        return users

    def create_books(self):
        """Create sample books"""
        books_data = [
            {
                'title': 'The Great Gatsby',
                'author': 'F. Scott Fitzgerald',
                'isbn': '9780743273565',
                'description': 'The Great Gatsby is a 1925 novel by American writer F. Scott Fitzgerald. Set in the Jazz Age on Long Island, near New York City, the novel depicts first-person narrator Nick Carraway\'s interactions with mysterious millionaire Jay Gatsby.',
                'category': 'Classic Literature',
                'published_date': date(1925, 4, 10),
                'available_copies': 5
            },
            {
                'title': 'To Kill a Mockingbird',
                'author': 'Harper Lee',
                'isbn': '9780061120084',
                'description': 'To Kill a Mockingbird is a novel by Harper Lee published in 1960. It was immediately successful, winning the Pulitzer Prize, and has become a classic of modern American literature.',
                'category': 'Classic Literature',
                'published_date': date(1960, 7, 11),
                'available_copies': 3
            },
            {
                'title': '1984',
                'author': 'George Orwell',
                'isbn': '9780451524935',
                'description': 'Nineteen Eighty-Four is a dystopian social science fiction novel and cautionary tale, written by English writer George Orwell. It was published in 1949 as Orwell\'s ninth and final book.',
                'category': 'Science Fiction',
                'published_date': date(1949, 6, 8),
                'available_copies': 4
            },
            {
                'title': 'Pride and Prejudice',
                'author': 'Jane Austen',
                'isbn': '9780141439518',
                'description': 'Pride and Prejudice is an 1813 novel of manners by Jane Austen. The novel follows the character development of Elizabeth Bennet, the dynamic protagonist who learns about the repercussions of hasty judgments.',
                'category': 'Romance',
                'published_date': date(1813, 1, 28),
                'available_copies': 6
            },
            {
                'title': 'The Catcher in the Rye',
                'author': 'J.D. Salinger',
                'isbn': '9780316769174',
                'description': 'The Catcher in the Rye is a novel by J. D. Salinger. A controversial novel originally published for adults, it has since become popular with adolescent readers for its themes of teenage angst and alienation.',
                'category': 'Coming of Age',
                'published_date': date(1951, 7, 16),
                'available_copies': 2
            },
            {
                'title': 'The Hobbit',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780547928227',
                'description': 'The Hobbit, or There and Back Again is a children\'s fantasy novel by English author J. R. R. Tolkien. It follows the quest of home-loving Bilbo Baggins to win a share of the treasure guarded by Smaug the dragon.',
                'category': 'Fantasy',
                'published_date': date(1937, 9, 21),
                'available_copies': 7
            },
            {
                'title': 'Harry Potter and the Philosopher\'s Stone',
                'author': 'J.K. Rowling',
                'isbn': '9780439708180',
                'description': 'Harry Potter and the Philosopher\'s Stone is a fantasy novel written by British author J. K. Rowling. The first novel in the Harry Potter series, it follows Harry Potter, a young wizard who discovers his magical heritage.',
                'category': 'Fantasy',
                'published_date': date(1997, 6, 26),
                'available_copies': 10
            },
            {
                'title': 'The Da Vinci Code',
                'author': 'Dan Brown',
                'isbn': '9780307474278',
                'description': 'The Da Vinci Code is a 2003 mystery thriller novel by Dan Brown. It follows symbologist Robert Langdon and cryptologist Sophie Neveu after a murder in the Louvre Museum in Paris.',
                'category': 'Mystery',
                'published_date': date(2003, 3, 18),
                'available_copies': 4
            },
            {
                'title': 'The Alchemist',
                'author': 'Paulo Coelho',
                'isbn': '9780062315007',
                'description': 'The Alchemist is a novel by Brazilian author Paulo Coelho that was first published in 1988. Originally written in Portuguese, it became a widely translated international bestseller.',
                'category': 'Philosophy',
                'published_date': date(1988, 4, 1),
                'available_copies': 5
            },
            {
                'title': 'The Lord of the Rings',
                'author': 'J.R.R. Tolkien',
                'isbn': '9780544003415',
                'description': 'The Lord of the Rings is an epic high-fantasy novel by English author J. R. R. Tolkien. Set in Middle-earth, it follows the quest to destroy the One Ring.',
                'category': 'Fantasy',
                'published_date': date(1954, 7, 29),
                'available_copies': 8
            }
        ]

        books = []
        for book_data in books_data:
            if not Book.objects.filter(isbn=book_data['isbn']).exists():
                book = Book.objects.create(**book_data)
                books.append(book)
                self.stdout.write(self.style.SUCCESS(f'  ✓ Created book: {book_data["title"]}'))

        return books

    def create_reviews(self, users, books):
        """Create sample reviews"""
        # Get regular users (exclude admin)
        regular_users = [user for username, user in users.items() if username not in ['admin']]

        if not regular_users or not books:
            self.stdout.write(self.style.WARNING('  No users or books available for reviews'))
            return

        reviews_data = [
            {
                'user': users.get('john_doe'),
                'book': books[0],  # The Great Gatsby
                'rating': 5,
                'review_text': 'An absolute masterpiece! The writing is beautiful and the story is captivating. A must-read for anyone interested in American literature.'
            },
            {
                'user': users.get('jane_smith'),
                'book': books[0],  # The Great Gatsby
                'rating': 4,
                'review_text': 'Great book with wonderful prose. The characters are complex and the themes are still relevant today.'
            },
            {
                'user': users.get('john_doe'),
                'book': books[1],  # To Kill a Mockingbird
                'rating': 5,
                'review_text': 'Powerful and moving. This book tackles important themes with grace and sensitivity. Highly recommended!'
            },
            {
                'user': users.get('bob_wilson'),
                'book': books[2],  # 1984
                'rating': 5,
                'review_text': 'Chilling and prophetic. Orwell\'s vision of a dystopian future is both terrifying and thought-provoking.'
            },
            {
                'user': users.get('jane_smith'),
                'book': books[3],  # Pride and Prejudice
                'rating': 4,
                'review_text': 'A delightful romance with wit and social commentary. Elizabeth Bennet is one of literature\'s greatest heroines.'
            },
            {
                'user': users.get('john_doe'),
                'book': books[6],  # Harry Potter
                'rating': 5,
                'review_text': 'Magical! This book sparked my love for reading. Perfect for all ages and a timeless classic.'
            },
            {
                'user': users.get('bob_wilson'),
                'book': books[6],  # Harry Potter
                'rating': 4,
                'review_text': 'Entertaining and imaginative. Great world-building and memorable characters.'
            },
            {
                'user': users.get('jane_smith'),
                'book': books[7],  # The Da Vinci Code
                'rating': 3,
                'review_text': 'Fast-paced thriller with interesting puzzles. Good for a light read, though some plot points are a bit far-fetched.'
            },
            {
                'user': users.get('staff'),
                'book': books[8],  # The Alchemist
                'rating': 5,
                'review_text': 'Inspiring and philosophical. This book reminds us to follow our dreams and listen to our hearts.'
            },
            {
                'user': users.get('bob_wilson'),
                'book': books[9],  # The Lord of the Rings
                'rating': 5,
                'review_text': 'Epic fantasy at its finest. The world-building is incredible and the story is unforgettable.'
            }
        ]

        review_count = 0
        for review_data in reviews_data:
            if review_data['user'] and review_data['book']:
                # Check if review already exists
                if not Review.objects.filter(
                    user=review_data['user'],
                    book=review_data['book']
                ).exists():
                    Review.objects.create(**review_data)
                    review_count += 1

        self.stdout.write(self.style.SUCCESS(f'  ✓ Created {review_count} reviews'))
