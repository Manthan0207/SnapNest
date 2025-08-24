# SnapNest 📸

> A modern photo management and sharing platform built with Django and Bootstrap

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-v3.8+-blue.svg)](https://www.python.org/downloads/)
[![Django](https://img.shields.io/badge/django-v4.0+-green.svg)](https://www.djangoproject.com/)
[![Bootstrap](https://img.shields.io/badge/bootstrap-v5.0+-purple.svg)](https://getbootstrap.com/)
[![GitHub stars](https://img.shields.io/github/stars/Manthan0207/SnapNest.svg)](https://github.com/Manthan0207/SnapNest/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/Manthan0207/SnapNest.svg)](https://github.com/Manthan0207/SnapNest/network)

## 🌟 Overview

SnapNest is a comprehensive photo management and sharing platform built with Django framework. It allows users to upload, organize, and share their memories with a clean, responsive interface powered by Bootstrap. The application focuses on simplicity, security, and user experience.

## ✨ Features

- **📱 Responsive Design** - Mobile-first design with Bootstrap 5
- **🔐 User Authentication** - Django's built-in authentication system
- **📸 Photo Upload & Management** - Easy drag & drop photo uploads
- **👥 User Profiles** - Personalized user profiles and dashboards
- **🔍 Search Functionality** - Search photos by title, tags, or description
- **💬 Social Features** - Like , Save Images
- **🎨 Modern UI/UX** - Clean interface with smooth Bootstrap animations
- **⚡ Fast Performance** - Optimized Django backend with efficient queries
- **🔒 Security** - CSRF protection, secure file uploads, and user permissions
- **🌙 Theme Support** - Light and dark mode toggle
- **📊 Dashboard** - User analytics and photo statistics

## 🛠️ Tech Stack

### Backend
- **Python 3.8+** - Programming language
- **Django 4.0+** - Web framework
- **SQLite/PostgreSQL** - Database

### Frontend
- **HTML5** - Markup language
- **CSS3** - Styling with custom properties
- **JavaScript (ES6+)** - Interactive functionality
- **Bootstrap 5** - CSS framework for responsive design
- **Font Awesome** - Icon library
- **jQuery** - DOM manipulation and AJAX calls

### Development Tools
- **pip** - Python package manager
- **virtualenv** - Virtual environment management
- **Django Debug Toolbar** - Development debugging



### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Manthan0207/SnapNest.git
   cd SnapNest
   ```

2. **Database Setup**
   ```bash

   python manage.py makemigrations
   python manage.py migrate
   ```

3. **Create Superuser** (Optional)
   ```bash
   python manage.py createsuperuser
   ```



4. **Run the Development Server**
   ```bash
   python manage.py runserver
   ```

5. **Open your browser**
   
   Navigate to `http://127.0.0.1:8000` to see SnapNest in action!
             # Django applications


### Database Configuration

### Media Files Setup

```python
# settings.py
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# URLs.py
from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

## 🎨 Frontend Features

### Bootstrap Components Used
- **Navbar** - Responsive navigation
- **Cards** - Photo display containers
- **Modal** - Photo lightbox and forms
- **Grid System** - Responsive photo galleries
- **Forms** - Styled upload and registration forms
- **Alerts** - User feedback messages

### Custom JavaScript Features
- **Photo Upload** - Drag & drop with preview
- **Image Lightbox** - Full-screen photo viewing
- **Infinite Scroll** - Dynamic content loading
- **Search Filter** - Real-time photo filtering

