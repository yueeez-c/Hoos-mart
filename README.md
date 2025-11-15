[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/k4pNZww7)

# Project B-17 - Sprint 4: Messaging + AWS S3 File Storage

A Django web application with real-time messaging, Google authentication, and AWS S3 cloud file storage for profile pictures and file uploads.

## 🚀 Quick Start

To run this locally, please run the following in your terminal:

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser  # optional
python manage.py runserver
```

## 📋 Features

### Core Features
- **Real-time Messaging** - Live chat system with channels and WebSocket support
- **Google Authentication** - Secure login via Google OAuth
- **AWS S3 Integration** - Cloud file storage for profile pictures and uploads
- **Profile Management** - Enhanced user profiles with image uploads
- **File Upload System** - Comprehensive file management with S3 storage
- **Responsive Design** - Modern, mobile-friendly interface

### NEW: Marketplace Features
- **Pickup Location Selector** - Sellers can specify safe pickup locations for exchanges (e.g., "UVA Library", "Student Union")
- **Donation/Free Category** - Special category for users to donate items or offer them for free
- **Enhanced Listing Management** - Create, edit, and delete marketplace listings with multiple photos

### NEW: Safety & Security
- **Scam/Fraud Warning System** - Track and flag suspicious user activity
  - `scam_warnings_count` - Number of warnings against a user
  - `is_flagged` - Account flagged for suspicious activity
  - Automatic warning banners for flagged users
- **User Verification** - Verified badge system for trusted users

### NEW: Advanced Messaging
- **Group Conversations** - Create and participate in group chats
  - Multi-participant support
  - Custom group names
  - Group-specific messaging features
- **Mute/Archive Conversations** - Better inbox management
  - `is_muted` - Silence notifications for specific conversations
  - `is_archived` - Hide conversations from main inbox
  - Quick access controls for conversation management

## ☁️ AWS S3 Setup Instructions

### 1. AWS Account Setup

1. **Create AWS Account**: Sign up at [aws.amazon.com](https://aws.amazon.com)
2. **Create IAM User**:
   - Go to IAM → Users → Create User
   - Attach policy: `AmazonS3FullAccess`
   - Generate Access Key and Secret Key
3. **Create S3 Bucket**:
   - Go to S3 → Create Bucket
   - Choose a unique bucket name (e.g., `your-project-b17-bucket`)
   - Set region (e.g., `us-east-1`)
   - Enable public read access for uploaded files

### 2. Environment Configuration

Create a `.env` file in your project root with the following:

```env
# AWS S3 Configuration
AWS_ACCESS_KEY_ID=your_aws_access_key_here
AWS_SECRET_ACCESS_KEY=your_aws_secret_key_here
AWS_STORAGE_BUCKET_NAME=your-bucket-name-here
AWS_S3_REGION_NAME=us-east-1
AWS_S3_USE_SSL=True

# Optional: Custom S3 settings
AWS_S3_CUSTOM_DOMAIN=your-bucket-name-here.s3.amazonaws.com
AWS_DEFAULT_ACL=public-read
```

### 3. Required Dependencies

The following packages are already included in `requirements.txt`:

```txt
boto3==1.35.80
django-storages==1.14.4
python-dotenv==1.0.1
```

### 4. Django Settings Configuration

The S3 integration is already configured in `config/settings.py`. The system automatically:

- **Uses S3** when AWS credentials are provided in `.env`
- **Falls back to local storage** when AWS credentials are missing
- **Handles media files** for profile pictures and uploads
- **Provides visual indicators** showing storage type (S3 vs Local)

## 🖼️ S3 Profile Picture System

### Features

- **Profile Picture Uploads**: Users can upload profile pictures stored in S3
- **Visual Storage Indicators**: Clear badges showing S3 vs Local storage
- **Image Validation**: Automatic validation for file types and sizes
- **User-Specific Paths**: Files organized by user ID for security

### Usage

1. **Upload Profile Picture**:
   - Navigate to `/user/profile/`
   - Click "Choose File" and select an image
   - Click "Update Profile" to save

2. **View S3 Demo**:
   - Navigate to `/user/s3-demo/`
   - See S3 configuration status
   - Test file uploads and view examples

### File Organization

```
S3 Bucket Structure:
├── user_1/
│   ├── profile_image.jpg
│   └── uploaded_file.pdf
├── user_2/
│   ├── profile_image.png
│   └── document.docx
└── ...
```

## 🛠️ Development Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your AWS credentials
# See "AWS S3 Setup Instructions" section above
```

### 3. Database Setup

```bash
# Run migrations
python manage.py migrate

# Create superuser (optional)
python manage.py createsuperuser
```

### 4. Run Development Server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` to access the application.

## 📱 Usage Guide

### Profile Management

1. **Sign Up/Login**: Use Google authentication or create account
2. **Update Profile**: Navigate to `/user/profile/`
3. **Upload Picture**: Select image file and save
4. **View Status**: See S3 storage badges indicating where files are stored

### S3 Demonstration

1. **S3 Demo Page**: Visit `/user/s3-demo/`
2. **Configuration Status**: View current AWS S3 settings
3. **Upload Examples**: Test different file types
4. **Storage Indicators**: See visual badges for S3 vs Local storage

### File Uploads

- **Supported Formats**: Images (JPG, PNG, GIF), Documents (PDF, DOCX, TXT)
- **Size Limits**: 10MB maximum per file
- **Security**: Files are organized by user ID
- **Access**: Public read access for uploaded images

### NEW: Marketplace Features

#### Creating Listings with Pickup Locations

1. **Navigate to Marketplace**: Go to `/marketplace/sell/`
2. **Fill Out Listing Form**:
   - Title, description, price, category
   - **NEW: Pickup Location** - Specify a safe meeting spot (e.g., "UVA Library Main Entrance", "Student Union Lobby")
3. **Upload Photos**: Select multiple images for your listing
4. **Select Category**:
   - Furniture, Electronics, Textbooks, Clothing, Other
   - **NEW: Donation/Free** - For items you want to give away

#### Donation/Free Items

- Select "Donation/Free" category when creating a listing
- Set price to $0.00 for free items
- Specify pickup location for safe exchange
- Help fellow students by donating items you no longer need

### NEW: Safety Features

#### Scam/Fraud Warning System

**For Buyers:**
- Check user profiles before making purchases
- Look for warning badges on seller profiles
- Report suspicious activity to administrators

**Warning Indicators:**
- 🚩 **Flagged Account** - User has been reported for suspicious activity
- ⚠️ **Warning Count** - Number of reports against the user
- ✅ **Verified Badge** - Trusted, verified users

**For Administrators:**
- Flag suspicious accounts via admin panel
- Track warning counts per user
- Review and moderate reported users

### NEW: Advanced Messaging Features

#### Group Conversations

1. **Create Group Chat**:
   - Navigate to messaging section
   - Select "Create Group" option
   - Add participants and set group name
2. **Manage Group**:
   - Add/remove participants
   - Rename group conversations
   - View all group members

#### Mute/Archive Conversations

**Mute Conversations:**
- Click the mute icon on any conversation
- Stop receiving notifications for that thread
- Messages still appear in your inbox
- Un-mute anytime to resume notifications

**Archive Conversations:**
- Archive old or completed conversations
- Remove from main inbox view
- Access archived conversations in "Archived" section
- Un-archive to bring back to main inbox

**Inbox Management:**
- Active conversations - Main inbox view
- Muted conversations - Visible with mute indicator
- Archived conversations - Hidden in separate "Archived" section
- Search and filter across all conversation types

## 🔧 Troubleshooting

### S3 Connection Issues

1. **Check Credentials**: Verify AWS keys in `.env` file
2. **Bucket Permissions**: Ensure bucket allows public read access
3. **Region Settings**: Confirm `AWS_S3_REGION_NAME` matches bucket region
4. **Fallback Mode**: System uses local storage when S3 unavailable

### Common Problems

- **Import Error**: Run `pip install -r requirements.txt`
- **Migration Issues**: Run `python manage.py migrate`
- **Static Files**: Run `python manage.py collectstatic` for production
- **Environment Variables**: Check `.env` file exists and has correct format

### Debug Mode

Check S3 status at `/user/s3-demo/` which shows:
- ✅ S3 Connected and Active
- ⚠️ S3 Configured but Inactive
- ❌ S3 Not Configured (Using Local Storage)

## 🚀 Production Deployment

### Heroku Deployment

1. **Set Environment Variables**:
   ```bash
   heroku config:set AWS_ACCESS_KEY_ID=your_key
   heroku config:set AWS_SECRET_ACCESS_KEY=your_secret
   heroku config:set AWS_STORAGE_BUCKET_NAME=your_bucket
   ```

2. **Configure Settings**: Production settings automatically detect S3 credentials

3. **Collect Static Files**: Run `python manage.py collectstatic`

### Security Notes

- **Never commit** `.env` files to git
- **Use IAM policies** to limit S3 permissions
- **Enable CORS** on S3 bucket for web uploads
- **Monitor usage** to avoid unexpected AWS charges

## 🤝 Team Development

### Git Workflow

```bash
# Pull latest changes
git pull origin main

# Make your changes
git add .
git commit -m "Description of changes"

# Push to repository
git push origin main
```

### Branch Protection

- `.env` files are automatically excluded via `.gitignore`
- Cache files (`__pycache__/`, `*.pyc`) are ignored
- Database files (`db.sqlite3`) are excluded

## 📖 API Documentation

### S3 Integration Endpoints

- `GET /user/profile/` - User profile with S3 upload form
- `POST /user/profile/` - Upload profile picture to S3
- `GET /user/s3-demo/` - S3 demonstration and status page

### Model Structure

```python
# User Profile with S3 Image and Safety Features
class Profile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to=user_directory_path)
    info = models.TextField(default='')
    is_student = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)  # NEW: Verified badge
    scam_warnings_count = models.PositiveIntegerField(default=0)  # NEW: Warning tracking
    is_flagged = models.BooleanField(default=False)  # NEW: Flagged for suspicious activity

# Marketplace Listing with Pickup Location
class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("furniture", "Furniture"),
        ("electronics", "Electronics"),
        ("textbooks", "Textbooks"),
        ("clothing", "Clothing"),
        ("donation", "Donation/Free"),  # NEW: Donation category
        ("other", "Other"),
    ]
    
    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    pickup_location = models.CharField(max_length=200, blank=True)  # NEW: Pickup location
    seller = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

# Messaging Thread with Group Support
class Thread(models.Model):
    participants = models.ManyToManyField(User, through="ThreadParticipant")
    context_listing = models.ForeignKey('Marketplace.Listing', null=True, blank=True)
    is_group = models.BooleanField(default=False)  # NEW: Group conversation flag
    group_name = models.CharField(max_length=100, blank=True)  # NEW: Group name
    created_at = models.DateTimeField(auto_now_add=True)

# Thread Participant with Mute/Archive
class ThreadParticipant(models.Model):
    thread = models.ForeignKey("Thread")
    user = models.ForeignKey(User)
    unread_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(null=True, blank=True)
    is_muted = models.BooleanField(default=False)  # NEW: Mute notifications
    is_archived = models.BooleanField(default=False)  # NEW: Archive conversation

# File Upload Tracking
class UserFile(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField()
```

### NEW Feature Endpoints

#### Marketplace
- `GET /marketplace/` - Browse listings with donation filter
- `POST /marketplace/sell/` - Create listing with pickup location
- `GET /marketplace/<id>/` - View listing details including pickup location

#### Safety & Moderation  
- Admin panel endpoints for flagging users
- User profile displays warning counts and verification status

#### Messaging
- Group conversation creation and management
- Mute/unmute conversation endpoints
- Archive/unarchive conversation endpoints
- Filtered inbox views (active, archived)

## 🎯 Sprint 4 Demonstration

### Key Features to Show

1. **S3 Configuration**: Display connection status and settings
2. **Profile Pictures**: Upload and view with storage indicators
3. **File Management**: Demonstrate upload system with metadata
4. **Visual Feedback**: Show S3 vs Local storage badges
5. **Pickup Locations**: Show safe exchange location selector
6. **Donation Category**: Demonstrate free/donation listings
7. **Safety Features**: Show scam warning system and user flagging
8. **Group Messaging**: Create and manage group conversations
9. **Mute/Archive**: Demonstrate conversation management features
10. **Team Integration**: Seamless integration with messaging and auth

### Demo Script

#### Part 1: S3 & Profile Features
1. Navigate to `/user/s3-demo/` - Show S3 status
2. Go to `/user/profile/` - Upload profile picture
3. View storage indicators - Demonstrate S3 vs Local badges

#### Part 2: Marketplace Enhancements
4. Go to `/marketplace/sell/` - Create new listing
5. Add pickup location - Show "UVA Library" example
6. Select "Donation/Free" category - Demonstrate free item posting
7. View listings - Show pickup location display

#### Part 3: Safety & Security
8. View user profile - Show warning indicators
9. Demonstrate flagging system - Admin panel
10. Check verified badges - Trust indicators

#### Part 4: Advanced Messaging
11. Create group conversation - Add multiple participants
12. Mute conversation - Disable notifications
13. Archive old threads - Clean inbox management
14. Un-archive and un-mute - Restore conversation

#### Part 5: Integration Testing
15. Test file uploads - Show different file types
16. Check messaging - Verify real-time functionality
17. Verify Google auth - Still working seamlessly
18. Confirm all features work together harmoniously

---

## 📞 Support

For questions about S3 setup, marketplace features, or implementation details, refer to:
- [Django Storages Documentation](https://django-storages.readthedocs.io/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
- [Django Messaging Documentation](https://docs.djangoproject.com/en/stable/)
- Project-specific questions: Check the code comments and model docstrings
