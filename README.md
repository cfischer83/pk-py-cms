# PK PY CMS

A modern, flexible Content Management System built with Django and Python. Think WordPress, but Python-powered.

## Features

- 📝 **Blog Posts & Pages** - Create and manage blog posts and static pages with a rich text editor
- 🖼️ **Media Library** - Upload and manage images, videos, documents, and other files
- 👥 **Multi-User Roles** - Admin, Editor, Author, and Contributor roles with different permissions
- 🏷️ **Categories & Tags** - Organize content with categories and tags
- 🔍 **SEO Ready** - Meta titles, descriptions, and Open Graph tags
- 📱 **Responsive Design** - Mobile-friendly templates with Tailwind CSS
- 🎨 **Multiple Templates** - Choose from different page templates (Default, Full Width, Landing, etc.)
- 🔐 **User Authentication** - Registration, login, password reset, and profile management

## Table of Contents

1. [Requirements](#requirements)
2. [Initial Setup](#initial-setup)
3. [Database Setup (PostgreSQL)](#database-setup-postgresql)
4. [Environment Configuration](#environment-configuration)
5. [Running the Server](#running-the-server)
6. [Development Tools](#development-tools)
7. [Project Structure](#project-structure)
8. [User Roles](#user-roles)
9. [Creating Content](#creating-content)
10. [Template Customization](#template-customization)
11. [Troubleshooting](#troubleshooting)

---

## Requirements

- Python 3.11+ (recommended: latest stable version)
- PostgreSQL 14+
- pip (Python package manager)
- Git

---

## Initial Setup

### 1. Install Python (if not installed)

**macOS:**
```bash
# Using Homebrew (recommended)
brew install python

# Verify installation
python3 --version
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

**Windows:**
Download from [python.org](https://www.python.org/downloads/) and run the installer.

### 2. Clone or Navigate to the Project

```bash
cd /path/to/dir/py-cms
```

### 3. Create a Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate

# Windows:
venv\Scripts\activate
```

> **Note:** You should see `(venv)` at the beginning of your terminal prompt when activated.

### 4. Install Dependencies

```bash
# For development (recommended)
pip install -r requirements/dev.txt

# For production
pip install -r requirements/prod.txt
```

### 5. Install Node.js Dependencies (for Tailwind CSS)

```bash
# Install Node.js if not already installed
# macOS:
brew install node

# Ubuntu/Debian:
sudo apt install nodejs npm

# Windows:
# Download from https://nodejs.org/

# Install Tailwind CSS and dependencies
npm install

# Build Tailwind CSS (first time)
npm run build
```

---

## Database Setup (PostgreSQL)

### 1. Install PostgreSQL

**macOS:**
```bash
# Using Homebrew
brew install postgresql@15
brew services start postgresql@15

# Add to PATH (add to ~/.zshrc or ~/.bash_profile)
echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

**Windows:**
Download from [postgresql.org](https://www.postgresql.org/download/windows/) and run the installer.

### 2. Create Database and User

```bash
# Access PostgreSQL prompt
# macOS:
psql postgres

# Linux:
sudo -u postgres psql
```

Then run these SQL commands:

```sql
-- Create the database
CREATE DATABASE pkpycms;

-- Create a user with password
CREATE USER pkpycms_user WITH PASSWORD 'your-secure-password-here';

-- Grant privileges
ALTER ROLE pkpycms_user SET client_encoding TO 'utf8';
ALTER ROLE pkpycms_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE pkpycms_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE pkpycms TO pkpycms_user;

-- Required for PostgreSQL 15+ (grant schema permissions)
GRANT ALL ON SCHEMA public TO pkpycms_user;
ALTER DATABASE pkpycms OWNER TO pkpycms_user;

-- Exit
\q
```

---

## Environment Configuration

### 1. Create Environment File

```bash
# Copy the example file
cp .env.example .env
```

### 2. Edit the .env File

Open `.env` in your editor and update these values:

```env
# Generate a new secret key (run this command and copy the output)
# python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
SECRET_KEY=your-generated-secret-key-here

# Set to False in production
DEBUG=True

# Your domain(s) - comma separated
ALLOWED_HOSTS=localhost,127.0.0.1

# Database credentials (must match what you created above)
DATABASE_NAME=pkpycms
DATABASE_USER=pkpycms_user
DATABASE_PASSWORD=your-secure-password-here
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Site settings
SITE_NAME=PK PY CMS
SITE_URL=http://localhost:8000
```

### 3. Apply Database Migrations

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux

# Run migrations
python manage.py migrate
```

### 4. Create Superuser (Admin Account)

```bash
python manage.py createsuperuser
```

Follow the prompts to enter your email, first name, last name, and password.

---

## Running the Server

### Start the Development Server

You'll need **two terminal windows/tabs** - one for Django and one for Tailwind CSS watching.

**Terminal 1 - Django Server:**
```bash
# Make sure virtual environment is activated
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate  # Windows

# Start the server
python manage.py runserver
```

**Terminal 2 - Tailwind CSS Watcher:**
```bash
# This watches your templates for changes and rebuilds CSS automatically
npm run dev
```

The site will be available at: **http://localhost:8000**

Admin panel: **http://localhost:8000/admin**

> **Note:** The Tailwind watcher will automatically rebuild CSS when you make changes to your templates. Just refresh your browser to see the changes.

### Production Build

For production, build minified CSS:
```bash
npm run build
```

### Start on a Different Port

```bash
python manage.py runserver 8080
```

### Start on All Network Interfaces

This allows other devices on your network to access the site:

```bash
python manage.py runserver 0.0.0.0:8000
```

Then access from other devices using your computer's IP address (e.g., `http://192.168.1.100:8000`)

### Stop the Server

Press `Ctrl+C` in the terminal where the server is running.

### Restart the Server

1. Stop the server with `Ctrl+C`
2. Run `python manage.py runserver` again

---

## Development Tools

### Django Debug Toolbar

When `DEBUG=True`, the debug toolbar appears on the right side of the browser. It shows:
- SQL queries
- Request/response data
- Template information
- Cache usage
- And more...

### Django Extensions

Useful management commands:

```bash
# Enhanced shell with auto-imports
python manage.py shell_plus

# Show all URLs
python manage.py show_urls

# Generate model graph (requires graphviz)
python manage.py graph_models -a -o models.png
```

### Code Formatting

```bash
# Format code with Black
black .

# Sort imports
isort .

# Check code style
flake8
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app tests
pytest apps/content/
```

---

## Project Structure

```
py-cms/
├── apps/                       # Django applications
│   ├── core/                   # Core utilities, home page
│   ├── users/                  # User authentication & profiles
│   ├── content/                # Posts, pages, categories, tags
│   └── media_library/          # Media file management
├── pkpycms/                    # Django project settings
│   ├── settings.py             # Main settings file
│   ├── urls.py                 # URL routing
│   └── wsgi.py                 # WSGI application
├── templates/                  # HTML templates
│   ├── base.html               # Base template
│   ├── core/                   # Core templates
│   ├── content/                # Content templates
│   │   └── pages/              # Page template variants
│   ├── users/                  # User templates
│   └── media_library/          # Media templates
├── static/                     # Static files (CSS, JS, images)
├── media/                      # User uploads (gitignored)
├── requirements/               # Python dependencies
│   ├── base.txt                # Base requirements
│   ├── dev.txt                 # Development requirements
│   └── prod.txt                # Production requirements
├── .env                        # Environment variables (gitignored)
├── .env.example                # Example environment file
├── .gitignore                  # Git ignore rules
├── manage.py                   # Django management script
└── README.md                   # This file
```

---

## User Roles

| Role | Permissions |
|------|-------------|
| **Admin** | Full access to everything |
| **Editor** | Can edit and publish all content |
| **Author** | Can create and edit own content, but cannot publish |
| **Contributor** | Can submit drafts for review |

### Assigning Roles

1. Go to Admin Panel → Users
2. Select a user
3. Change their "Role" field
4. Save

---

## Creating Content

### Blog Posts

1. Go to Admin Panel → Posts → Add Post
2. Fill in:
   - **Title**: The post title
   - **Slug**: URL-friendly version (auto-generated)
   - **Content**: Rich text content using the Quill editor
   - **Excerpt**: Short summary for listings
   - **Categories/Tags**: Organize your post
   - **Featured Image**: Select from Media Library
   - **Status**: Draft, Pending, Published, or Archived
3. Save

### Pages

1. Go to Admin Panel → Pages → Add Page
2. Choose a **Template**:
   - Default: Standard page layout
   - Full Width: No max-width container
   - Landing: Hero section with featured image
   - Sidebar Left/Right: With sidebar (future)
3. Fill in content and save

### Media

1. Go to Media Library (in navigation when logged in)
2. Click "Upload Media"
3. Select file, add title/alt text/caption
4. Upload

Or use Admin Panel → Media → Add Media

---

## Template Customization

### Customizing CSS

#### Custom Styles

Edit `static/css/custom.css` for custom CSS classes like buttons, forms, etc.

```css
/* Example: Modify button padding */
.btn {
    padding: 1.5rem 2rem;  /* Change this */
}
```

Changes to `custom.css` will be reflected immediately after browser refresh (no rebuild needed).

#### Tailwind Utility Classes

Use Tailwind utility classes directly in your templates:

```html
<div class="bg-primary-500 text-white p-4 rounded-lg">
    Hello World
</div>
```

The Tailwind watcher will detect these classes and include them in the compiled CSS.

#### Changing Theme Colors

Edit `tailwind.config.js` to change the color palette:

```javascript
colors: {
    primary: {
        500: '#008c95',  // Change this
        // ...
    }
}
```

After changing the config, Tailwind will automatically rebuild (if `npm run dev` is running).

#### CSS File Structure

- **`static/css/custom.css`** - Your custom styles (buttons, forms, prose, etc.)
- **`static/css/tailwind.input.css`** - Tailwind directives (don't modify)
- **`static/css/tw-compiled.css`** - Generated file (gitignored, auto-generated)
- **`tailwind.config.js`** - Tailwind configuration (colors, plugins, etc.)

### Creating a New Page Template

1. Create a new file in `templates/content/pages/`:

```html
<!-- templates/content/pages/my-template.html -->
{% extends 'base.html' %}

{% block content %}
<!-- Your custom layout here -->
<div class="my-custom-layout">
    <h1>{{ page.title }}</h1>
    {{ page.content.html|safe }}
</div>
{% endblock %}
```

2. Add the template choice in `apps/content/models.py`:

```python
TEMPLATE_CHOICES = [
    ('default', 'Default'),
    ('full-width', 'Full Width'),
    ('my-template', 'My Template'),  # Add this
    # ...
]
```

3. Run migrations if you changed model choices:

```bash
python manage.py makemigrations
python manage.py migrate
```

### Page Template Configuration

#### Creating a New Page Template

1. Create a new file in `templates/content/pages/`:

### "No module named 'django'"
```bash
# Make sure virtual environment is activated
source venv/bin/activate
pip install -r requirements/dev.txt
```

### Database Connection Error
1. Check PostgreSQL is running:
   ```bash
   # macOS
   brew services list
   
   # Linux
   sudo systemctl status postgresql
   ```

2. Verify credentials in `.env` match your database setup

3. Make sure the database exists:
   ```bash
   psql -U pkpycms_user -d pkpycms -h localhost
   ```

### "Relation does not exist"
Run migrations:
```bash
python manage.py migrate
```

### Static Files Not Loading
```bash
# Collect static files (production)
python manage.py collectstatic

# Or in development, make sure DEBUG=True
```

### Port Already in Use
```bash
# Find and kill the process
lsof -i :8000
kill -9 <PID>

# Or use a different port
python manage.py runserver 8080
```

---

## Useful Commands Reference

| Command | Description |
|---------|-------------|
| `python manage.py runserver` | Start development server |
| `python manage.py migrate` | Apply database migrations |
| `python manage.py makemigrations` | Create new migrations |
| `python manage.py createsuperuser` | Create admin user |
| `python manage.py collectstatic` | Collect static files |
| `python manage.py shell` | Django shell |
| `python manage.py shell_plus` | Enhanced shell (dev only) |
| `python manage.py dbshell` | Database shell |
| `python manage.py test` | Run tests |

---

## Setting Up on Another Device

1. Clone/copy the project
2. Install Python 3.11+
3. Install PostgreSQL
4. Create virtual environment: `python3 -m venv venv`
5. Activate: `source venv/bin/activate`
6. Install dependencies: `pip install -r requirements/dev.txt`
7. Copy `.env.example` to `.env` and configure
8. Create database and user (see [Database Setup](#database-setup-postgresql))
9. Run migrations: `python manage.py migrate`
10. Create superuser: `python manage.py createsuperuser`
11. Start server: `python manage.py runserver`

---

## License

This project is private and proprietary.

---

## Support

For issues or questions, please contact the development team.
