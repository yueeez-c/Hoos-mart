# Project B-17 - UVA Marketplace Platform

**A comprehensive Django web application featuring a student marketplace, real-time messaging, Google authentication, AWS S3 cloud storage, and robust moderation tools.**

[![Django](https://img.shields.io/badge/Django-5.2.6-green.svg)](https://www.djangoproject.com/)
[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Production-blue.svg)](https://www.postgresql.org/)
[![Heroku](https://img.shields.io/badge/Deployed-Heroku-purple.svg)](https://www.heroku.com/)

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Live Demo](#-live-demo)
- [Features](#-features)
- [Technology Stack](#-technology-stack)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Deployment](#-deployment)
- [Usage Guide](#-usage-guide)
- [Troubleshooting](#-troubleshooting)
- [Contributing Team AND Sources](#-contributing-team)

---

## Overview

Project B-17 is a full-featured student marketplace platform designed for the UVA community. Students can buy, sell, and donate items, communicate securely through real-time messaging, and manage their profiles with cloud-stored media. The platform includes comprehensive moderation tools, user verification, and safety features to ensure a secure trading environment.

### **Live Demo**
**Production URL:** [https://shrouded-sea-15354-cd819052cb94.herokuapp.com/](https://shrouded-sea-15354-cd819052cb94.herokuapp.com/)

Note: To view the moderator functions use the following seeded moderator account:
User: deployed_admin
Password: Moderator123


---

## Features

###  **Marketplace**
- **Buy & Sell Items: Full-featured marketplace with categories (Furniture, Electronics, Textbooks, Clothing, Donation/Free, Other)
- **Multiple Image Upload** - Interactive carousel with navigation for up to multiple photos per listing
- **Pickup Location Selector** - Safe, predefined campus locations for item exchanges
- **Advanced Search & Filters** - Filter by category, price range, status, and seller
- **Listing Management** - Create, edit, delete, and update listing status (Available/Sold/Pending)

### 💬 **Real-Time Messaging**
- **Live Chat System** - WebSocket-powered messaging using Django Channels
- **Group Conversations** - Multi-user group chats with custom names
- **Message from Listings** - Direct messaging integrated with marketplace
- **Conversation Management** - Mute notifications, archive chats, organize inbox
- **Unread Indicators** - Visual badges for unread message counts

### 🔐 **Authentication & Security**
- **Google OAuth** - Secure login with UVA Google accounts (@virginia.edu)
- **Email Verification** - Required email confirmation for new accounts
- **School Email Validation** - Restricted to verified university domains
- **User Verification System** - Badge system for trusted users

### 👤 **User Profiles**
- **Profile Customization** - Bio, location, and cloud-stored profile pictures
- **AWS S3 Integration** - Automatic cloud storage for all profile images
- **Activity Tracking** - View user's listings, ratings, and history
- **Profile Completion** - Middleware ensures complete user profiles

### 🛡️ **Moderation & Safety**
- **Report System** - Report listings and users for violations
- **Ban System** - Admin tools to ban and manage problematic users
- **Banned User Database** - Email-based tracking to prevent re-registration
- **Automatic Flagging** - Multi-report users are automatically flagged
- **Admin Dashboard** - Comprehensive moderation panel

### 📁 **File Management**
- **AWS S3 Cloud Storage** - Scalable cloud storage for all media
- **File Validation** - Automatic type, size, and format validation
- **Smart Organization** - User-specific file paths for security
- **Fallback Storage** - Local storage when S3 is unavailable

---

## 🛠️ Technology Stack

### **Backend**
- Django 5.2.6 - Python web framework
- Django Channels - WebSocket support
- PostgreSQL - Production database
- Django REST Framework - API endpoints
- Psycopg - PostgreSQL adapter

### **Frontend**
- Bootstrap 5 - Responsive CSS framework
- JavaScript (ES6+) - Interactive components
- WebSockets - Real-time messaging

### **Cloud Services**
- AWS S3 - Object storage
- Boto3 - AWS SDK
- Django Storages - S3 integration

### **Authentication**
- Google OAuth 2.0 - via django-allauth
- SendGrid - Email delivery

### **Deployment**
- Heroku - Cloud hosting
- Gunicorn - WSGI server
- WhiteNoise - Static files
- Redis - Channel layer (production)

---

## 🚀 Quick Start

### **Prerequisites**
- Python 3.13+
- Git
- (Optional) PostgreSQL for local development
- (Optional) AWS account for S3 storage

### **Installation**

```bash
# 1. Clone repository
git clone https://github.com/uva-cs3240-f25/project-b-17.git
cd project-b-17

# 2. Create virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables (create .env file - see Configuration section)

# 5. Run migrations
python manage.py migrate

# 6. Create superuser (optional)
python manage.py createsuperuser

# 7. Collect static files
python manage.py collectstatic --no-input

# 8. Run development server
python manage.py runserver
```

Access at `http://localhost:8000`

---

## ⚙️ Configuration

### **Environment Variables**

Create a `.env` file in project root:

```env
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (optional for local - SQLite used by default)
DATABASE_URL=postgres://user:password@localhost:5432/dbname

# AWS S3 (optional - falls back to local storage)
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-east-1

# Google OAuth
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Email (SendGrid)
EMAIL_HOST=smtp.sendgrid.net
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=your-sendgrid-api-key
EMAIL_PORT=587
DEFAULT_FROM_EMAIL=noreply@yourdomain.com
```

### **AWS S3 Setup**

1. Create AWS account at [aws.amazon.com](https://aws.amazon.com)
2. Create IAM User with `AmazonS3FullAccess` policy
3. Create S3 Bucket in desired region
4. Add credentials to `.env` file

### **Google OAuth Setup**

1. Visit [console.cloud.google.com](https://console.cloud.google.com)
2. Create new project
3. Enable Google+ API
4. Create OAuth 2.0 Client ID
5. Add authorized redirect URIs:
   - `http://localhost:8000/accounts/google/login/callback/`
   - `https://your-domain.herokuapp.com/accounts/google/login/callback/`
6. Add credentials to `.env` file

---

## 📁 Project Structure

```
project-b-17/
├── config/                 # Project configuration
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL configuration
│   ├── wsgi.py            # WSGI configuration
│   ├── asgi.py            # ASGI configuration (WebSockets)
│   ├── db_middleware.py   # Database connection middleware
│   └── storage_backends.py # AWS S3 storage backends
│
├── home/                   # Homepage app
│   ├── views.py           # Homepage views
│   ├── templates/         # Homepage templates
│   └── static/            # Homepage static files
│
├── marketplace/            # Marketplace app
│   ├── models.py          # Listing and ListingImage models
│   ├── views.py           # Marketplace views
│   ├── forms.py           # Marketplace forms
│   ├── urls.py            # Marketplace URLs
│   ├── templates/         # Marketplace templates
│   └── management/        # Custom management commands
│
├── messaging/              # Real-time messaging app
│   ├── models.py          # Conversation and Message models
│   ├── views.py           # Messaging views
│   ├── consumers.py       # WebSocket consumers
│   └── templates/         # Messaging templates
│
├── user/                   # User management app
│   ├── models.py          # Profile and BannedUser models
│   ├── views.py           # User views
│   ├── forms.py           # User forms
│   ├── validators.py      # Email validation
│   ├── middleware.py      # Profile completion middleware
│   ├── adapter.py         # Social account adapter
│   └── templates/         # User templates
│
├── reports/                # Moderation and reporting app
│   ├── models.py          # Report models
│   ├── views.py           # Moderation views
│   └── templates/         # Report templates
│
├── staticfiles/            # Collected static files
├── media/                  # Local media files (if not using S3)
├── requirements.txt        # Python dependencies
├── runtime.txt             # Python version for Heroku
├── Procfile                # Heroku process configuration
├── manage.py               # Django management script
└── README.md               # This file
```

---

## 🚢 Deployment

### **Heroku Deployment**

The project auto-deploys to Heroku when pushing to the `main` branch on GitHub.

**Manual deployment:**

```bash
# Login to Heroku
heroku login

# Add Heroku remote (if not already added)
heroku git:remote -a shrouded-sea-15354

# Deploy
git push heroku main

# Run migrations
heroku run python manage.py migrate -a shrouded-sea-15354

# Create superuser
heroku run python manage.py createsuperuser -a shrouded-sea-15354
```

**Set environment variables on Heroku:**

```bash
heroku config:set SECRET_KEY=your-secret-key -a shrouded-sea-15354
heroku config:set AWS_ACCESS_KEY_ID=your-key -a shrouded-sea-15354
heroku config:set AWS_SECRET_ACCESS_KEY=your-secret -a shrouded-sea-15354
heroku config:set AWS_STORAGE_BUCKET_NAME=your-bucket -a shrouded-sea-15354
```

**View logs:**

```bash
heroku logs --tail -a shrouded-sea-15354
```

---

## 📚 Usage Guide

### **Creating a Marketplace Listing**

1. Log in with Google account
2. Navigate to **Marketplace → Sell**
3. Fill out listing details:
   - Title and description
   - Price
   - Category (Furniture, Electronics, etc.)
   - Pickup location (UVA Library, Student Union, etc.)
4. Upload up to multiple images
5. Click **Create Listing**

### **Browsing & Buying**

1. Navigate to **Marketplace → Buy**
2. Use filters to narrow search:
   - Category dropdown
   - Price range
   - Search by keyword
3. Click on listing to view details
4. Use carousel to view all images
5. Click **Message Seller** to inquire

### **Messaging**

1. Click **Message Seller** from any listing
2. Type message and send
3. View conversations in **Messages** inbox
4. **Mute** conversations to disable notifications
5. **Archive** old conversations to clean inbox

### **Profile Management**

1. Navigate to **Profile**
2. Upload profile picture (stored in AWS S3)
3. Update bio and location
4. View your active listings

### **Reporting & Safety**

1. Click **Report** on problematic listings
2. Select violation type
3. Submit with optional details
4. Admins review reports in dashboard

---

## 🐛 Troubleshooting

### **Common Issues**

**Images not loading:**
- Check AWS S3 credentials in `.env`
- Verify bucket permissions
- Check CORS configuration on S3 bucket

**Database errors on Heroku:**
- Run migrations: `heroku run python manage.py migrate -a shrouded-sea-15354`
- Check database connection: `heroku pg:info -a shrouded-sea-15354`

**"Missing table" errors:**
- Run: `heroku run python manage.py create_banneduser_table -a shrouded-sea-15354`
- Re-run migrations

**WebSocket connection failed:**
- Check Redis configuration
- Verify ASGI settings
- Review channel layer configuration

**Static files not loading:**
- Run: `python manage.py collectstatic`
- Check WhiteNoise configuration

---

## 👥 Contributing Team

**UVA CS 3240 - Fall 2025**
- Team B-17

---

## � Citations & References

### **Frameworks & Libraries**

1. **Django Web Framework**
   - Django Software Foundation. (2025). *Django: The Web framework for perfectionists with deadlines* (Version 5.2.6) [Software]. https://www.djangoproject.com/
   - Documentation: https://docs.djangoproject.com/

2. **Django Channels**
   - Django Software Foundation. (2025). *Django Channels: WebSocket and asynchronous support for Django* [Software]. https://channels.readthedocs.io/
   - Used for real-time messaging functionality

3. **Django Allauth**
   - Penners, R. (2025). *django-allauth: Integrated set of Django applications addressing authentication* [Software]. https://django-allauth.readthedocs.io/
   - Used for Google OAuth integration

4. **Django Storages**
   - jschneier. (2025). *django-storages: Custom storage backends for Django* [Software]. https://django-storages.readthedocs.io/
   - Used for AWS S3 integration

5. **Bootstrap**
   - Bootstrap Team. (2025). *Bootstrap: The most popular HTML, CSS, and JS library* (Version 5.x) [Software]. https://getbootstrap.com/
   - Used for responsive UI design

### **Cloud Services**

6. **Amazon Web Services (AWS)**
   - Amazon Web Services, Inc. (2025). *Amazon S3: Object storage built to retrieve any amount of data from anywhere*. https://aws.amazon.com/s3/
   - AWS Documentation: https://docs.aws.amazon.com/

7. **Boto3 (AWS SDK for Python)**
   - Amazon Web Services, Inc. (2025). *Boto3: AWS SDK for Python* [Software]. https://boto3.amazonaws.com/
   - Used for S3 integration and file management

8. **Heroku**
   - Salesforce, Inc. (2025). *Heroku: Cloud Application Platform*. https://www.heroku.com/
   - Platform for production deployment

### **Database**

9. **PostgreSQL**
   - PostgreSQL Global Development Group. (2025). *PostgreSQL: The World's Most Advanced Open Source Relational Database*. https://www.postgresql.org/
   - Production database system

10. **Psycopg**
    - Di Gregorio, F., & Varrazzo, D. (2025). *Psycopg: PostgreSQL adapter for Python* [Software]. https://www.psycopg.org/
    - Database adapter for Django

### **Python Packages**

11. **Gunicorn**
    - Chesneau, B. (2025). *Gunicorn: Python WSGI HTTP Server for UNIX* [Software]. https://gunicorn.org/
    - Production WSGI server

12. **WhiteNoise**
    - Evans, D. (2025). *WhiteNoise: Radically simplified static file serving for Python web apps* [Software]. http://whitenoise.evans.io/
    - Static file serving

13. **Pillow**
    - Clark, A., et al. (2025). *Pillow: Python Imaging Library* [Software]. https://python-pillow.org/
    - Image processing and validation

### **Email Services**

14. **SendGrid**
    - Twilio Inc. (2025). *SendGrid: Email Delivery Service*. https://sendgrid.com/
    - Transactional email delivery

### **Authentication**

15. **Google OAuth 2.0**
    - Google LLC. (2025). *Google Identity Platform: OAuth 2.0 for Web Server Applications*. https://developers.google.com/identity/protocols/oauth2
    - Social authentication provider

### **Additional Tools**

16. **Python-dotenv**
    - Pedregosa, S. (2025). *python-dotenv: Read key-value pairs from .env file* [Software]. https://github.com/theskumar/python-dotenv
    - Environment variable management

17. **Django Crispy Forms**
    - Pons, M. (2025). *django-crispy-forms: Best way to have Django DRY forms* [Software]. https://django-crispy-forms.readthedocs.io/
    - Form rendering and styling

### **Learning Resources**

18. **Django Documentation**
    - Django Software Foundation. (2025). *Django Documentation*. https://docs.djangoproject.com/en/stable/
    - Official Django tutorials and API reference

19. **MDN Web Docs**
    - Mozilla Corporation. (2025). *MDN Web Docs: Resources for developers, by developers*. https://developer.mozilla.org/
    - HTML, CSS, and JavaScript references

20. **Bootstrap Documentation**
    - Bootstrap Team. (2025). *Bootstrap Documentation*. https://getbootstrap.com/docs/5.3/
    - UI component implementation guides

### **Course Materials**

21. **UVA CS 3240 Course Materials**
    - University of Virginia, Department of Computer Science. (2025). *CS 3240: Advanced Software Development*
    - Course lectures, labs, and project requirements

---

## License

This project is developed for UVA CS 3240 coursework. All external libraries and frameworks are used in accordance with their respective licenses:

- **Django**: BSD 3-Clause License
- **Bootstrap**: MIT License
- **Django Channels**: BSD License
- **Django Allauth**: MIT License
- **Boto3**: Apache License 2.0
- **PostgreSQL**: PostgreSQL License
- **Pillow**: HPND License

All proprietary code developed by Team B-17 is for educational purposes as part of UVA CS 3240.

---

## Support & Documentation

### **Official Documentation**
- **Django Documentation:** [docs.djangoproject.com](https://docs.djangoproject.com/)
- **Django Channels:** [channels.readthedocs.io](https://channels.readthedocs.io/)
- **Django Storages:** [django-storages.readthedocs.io](https://django-storages.readthedocs.io/)
- **AWS S3 Documentation:** [docs.aws.amazon.com/s3/](https://docs.aws.amazon.com/s3/)
- **Boto3 Documentation:** [boto3.amazonaws.com](https://boto3.amazonaws.com/)
- **Heroku Documentation:** [devcenter.heroku.com](https://devcenter.heroku.com/)
- **Bootstrap Documentation:** [getbootstrap.com/docs](https://getbootstrap.com/docs/)
- **PostgreSQL Documentation:** [postgresql.org/docs](https://www.postgresql.org/docs/)

### **Online Resources**
- **Stack Overflow:** [stackoverflow.com](https://stackoverflow.com/)
- **Django Forum:** [forum.djangoproject.com](https://forum.djangoproject.com/)
- **GitHub Issues:** Project-specific issues and discussions

##Generative AI Resources
- ChatGPT version 5.1
- Microsoft Copilot
- Google Gemini 



**Made with by Team B-17**

*University of Virginia | CS 3240 - Advanced Software Development | Fall 2025
