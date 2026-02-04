# Libms - Library Management System

A comprehensive Django-based library management system with user authentication, book management, reviews, and administrative features.

## Features

- User authentication (registration, login, password reset)
- Book catalog management
- Book search functionality
- User reviews and ratings
- Staff dashboard for library management
- User profiles
- Responsive UI with modern design

## Quick Start

**TL;DR - Get started in 5 minutes:**

```bash
# 1. Install dependencies (no virtual environment needed)
pip install django mysqlclient pillow

# 2. Create MySQL database
mysql -u root -p -e "CREATE DATABASE libms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 3. Configure environment
cp .env.example .env
# Edit .env with your MySQL password

# 4. Setup database and seed with sample data
python manage.py migrate
python manage.py seed_data

# 5. Run server
python manage.py runserver
```

**Access the app at:** http://127.0.0.1:8000/

**Login with:** `admin` / `admin123` or `staff` / `staff123`

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Database Seeding](#database-seeding)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Common Commands](#common-commands)
- [Troubleshooting](#troubleshooting)
- [Technologies Used](#technologies-used)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.8 or higher
- MySQL Server 5.7 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone git@github.com:hareom284/Libms.git
cd Libms
```

### 2. Install Dependencies

```bash
pip install django
pip install mysqlclient
pip install pillow
```

### 3. Database Setup

#### Create MySQL Database

```sql
# Login to MySQL
mysql -u root -p

# Create database
CREATE DATABASE libms CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# Create user (optional but recommended)
CREATE USER 'libms_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON libms.* TO 'libms_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 4. Environment Configuration

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit the `.env` file with your configuration:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True

# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=libms
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306

# Email Configuration (for password reset)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Important Notes:**
- Generate a new SECRET_KEY for production
- For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833)
- Never commit your `.env` file to version control

### 5. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Seed Database with Default Records (Recommended)

Populate the database with sample data for testing:

```bash
python manage.py seed_data
```

This will create:
- **Users:** Admin, staff member, and 3 regular users
- **Books:** 10 sample books across different categories
- **Reviews:** Sample reviews and ratings for books

**Default Login Credentials:**
- Admin: `admin` / `admin123`
- Staff: `staff` / `staff123`
- User 1: `john_doe` / `user123`
- User 2: `jane_smith` / `user123`
- User 3: `bob_wilson` / `user123`

### 7. Create Superuser (Alternative to Seeder)

If you prefer to create your own admin account instead of using the seeder:

```bash
python manage.py createsuperuser
```

Follow the prompts to create a custom admin account.

### 8. Collect Static Files

```bash
python manage.py collectstatic
```

### 9. Run Development Server

```bash
python manage.py runserver
```

The application will be available at `http://127.0.0.1:8000/`

---

## Database Seeding

The `seed_data` management command provides an easy way to populate your database with sample data for testing and development.

### What Gets Created

**Users (5 total):**
- 1 Admin (superuser with full access)
- 1 Staff member (can manage books)
- 3 Regular users (can browse and review)

**Books (10 total):**
- The Great Gatsby by F. Scott Fitzgerald
- To Kill a Mockingbird by Harper Lee
- 1984 by George Orwell
- Pride and Prejudice by Jane Austen
- The Catcher in the Rye by J.D. Salinger
- The Hobbit by J.R.R. Tolkien
- Harry Potter and the Philosopher's Stone by J.K. Rowling
- The Da Vinci Code by Dan Brown
- The Alchemist by Paulo Coelho
- The Lord of the Rings by J.R.R. Tolkien

**Reviews:**
- Multiple reviews across different books
- Varied ratings (3-5 stars)
- Detailed review text

### Important Notes

- The seeder clears existing data (Reviews, Books, and non-superuser accounts)
- If you want to keep existing data, comment out the delete statements in `seed_data.py`
- Run the seeder after migrations but before adding your own data
- Default passwords are for development only - change them in production

---

## Usage

### Accessing the Application

- **Homepage:** http://127.0.0.1:8000/
- **Admin Panel:** http://127.0.0.1:8000/admin/
- **User Registration:** http://127.0.0.1:8000/register/
- **Login:** http://127.0.0.1:8000/login/

### User Roles

1. **Regular Users:**
   - Browse and search books
   - View book details
   - Write and edit reviews
   - Manage profile

2. **Staff Users:**
   - All regular user privileges
   - Add, edit, and delete books
   - Access staff dashboard
   - Manage library catalog

3. **Admin Users:**
   - All staff privileges
   - Access Django admin panel
   - Manage users and permissions
   - Full system control

---

## Project Structure

```
Libms/
├── libms/                  # Project settings
│   ├── settings.py         # Main configuration
│   ├── urls.py             # Root URL configuration
│   └── wsgi.py             # WSGI configuration
├── library/                # Main application
│   ├── admin/              # Admin configurations
│   ├── forms/              # Form definitions
│   ├── models/             # Database models
│   │   ├── book.py         # Book model
│   │   ├── review.py       # Review model
│   │   └── user.py         # User profile model
│   ├── views/              # View logic
│   ├── urls/               # URL routing
│   ├── templates/          # HTML templates
│   │   ├── auth/           # Authentication templates
│   │   ├── books/          # Book-related templates
│   │   ├── reviews/        # Review templates
│   │   └── users/          # User profile templates
│   └── management/         # Custom management commands
│       └── commands/
│           └── seed_data.py # Database seeder
├── static/                 # Static files (CSS, JS, images)
├── media/                  # User-uploaded files
├── manage.py               # Django management script
├── .env                    # Environment variables (not in git)
├── .env.example            # Example environment file
└── README.md               # This file
```

---

## Common Commands

```bash
# Run development server
python manage.py runserver

# Run on different port
python manage.py runserver 8080

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Seed database with sample data
python manage.py seed_data

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Open Django shell
python manage.py shell

# Check for issues
python manage.py check
```

---

## Troubleshooting

### Database Connection Issues

If you encounter database connection errors:

1. Verify MySQL is running: `mysql -u root -p`
2. Check database credentials in `.env`
3. Ensure the database exists: `SHOW DATABASES;`
4. Check MySQL user permissions
5. Verify `mysqlclient` is installed: `pip install mysqlclient`

### Missing Dependencies

```bash
# Install all dependencies
pip install django mysqlclient pillow
```

### Static Files Not Loading

```bash
python manage.py collectstatic --clear
python manage.py collectstatic
```

### Migration Issues

```bash
# Reset migrations (CAUTION: This will delete data)
python manage.py migrate library zero
python manage.py migrate
```

### Port Already in Use

If port 8000 is already in use:

```bash
# Use a different port
python manage.py runserver 8080
```

### ImportError or ModuleNotFoundError

Make sure you're in the correct directory and all dependencies are installed:

```bash
cd Libms
pip install django mysqlclient pillow
python manage.py runserver
```

---

## Email Configuration

For password reset functionality to work:

### Gmail Users

1. Enable 2-factor authentication
2. Create an [App Password](https://support.google.com/accounts/answer/185833)
3. Use the app password in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### Development/Testing

Use console backend for development (emails print to console):

```env
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

---

## Technologies Used

- **Backend:** Django 4.x (Python)
- **Database:** MySQL 5.7+
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Image Processing:** Pillow
- **Version Control:** Git & GitHub
- **AI Development Tools:** Claude Code, GitHub Copilot, Google Gemini
- **Package Management:** pip

---

## Development

### Adding a New Book

1. Login as staff user (`staff` / `staff123`)
2. Navigate to Staff Dashboard
3. Click "Add New Book"
4. Fill in required fields:
   - Title
   - Author
   - ISBN (13 digits)
   - Description
   - Category
   - Publication Date
   - Available Copies
5. Upload cover image (optional)
6. Submit

### Writing Reviews

1. Login as any user
2. Navigate to book detail page
3. Click "Add Review"
4. Select rating (1-5 stars)
5. Write review text
6. Submit

### Editing Your Review

1. Login and navigate to your review
2. Click "Edit"
3. Update rating or review text
4. Save changes

---

## Additional Documentation

- `ASSIGNMENT_DOCUMENTATION.md` - Detailed assignment documentation
- `DESIGN_DOCUMENTATION.md` - Design and architecture documentation
- `PROJECT_PLANNING.md` - Project planning and requirements
- `UI_CUSTOMIZATION_GUIDE.md` - UI customization guidelines

---

## Contributing

This is an educational project. If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

This project is for educational purposes only.

---

## Support

For issues and questions:
- Check the [Troubleshooting](#troubleshooting) section
- Review the documentation
- Contact the development team
- Open an issue on GitHub

---

## Acknowledgments

- Built with assistance from **Claude Code**, **GitHub Copilot**, and **Google Gemini**
- Django community for excellent documentation and tutorials
- Open source contributors and the Python community
- Educational institution for project guidance

---

## Changelog

### Version 1.0.0
- Initial release
- User authentication system
- Book management functionality
- Review and rating system
- Database seeder with sample data
- Responsive UI design

---

**Made with assistance from AI coding tools | Django + MySQL | Educational Project**
