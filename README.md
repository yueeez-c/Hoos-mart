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

- **Real-time Messaging** - Live chat system with channels and WebSocket support
- **Google Authentication** - Secure login via Google OAuth
- **AWS S3 Integration** - Cloud file storage for profile pictures and uploads
- **Profile Management** - Enhanced user profiles with image uploads
- **File Upload System** - Comprehensive file management with S3 storage
- **Responsive Design** - Modern, mobile-friendly interface

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
# User Profile with S3 Image
class Profile(models.Model):
    user = models.OneToOneField(User)
    image = models.ImageField(upload_to=user_directory_path)
    info = models.TextField(default='')
    is_student = models.BooleanField(default=True)

# File Upload Tracking
class UserFile(models.Model):
    user = models.ForeignKey(User)
    file = models.FileField(upload_to=user_directory_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    file_size = models.PositiveIntegerField()
```

## 🎯 Sprint 4 Demonstration

### Key Features to Show

1. **S3 Configuration**: Display connection status and settings
2. **Profile Pictures**: Upload and view with storage indicators
3. **File Management**: Demonstrate upload system with metadata
4. **Visual Feedback**: Show S3 vs Local storage badges
5. **Team Integration**: Seamless integration with messaging and auth

### Demo Script

1. Navigate to `/user/s3-demo/` - Show S3 status
2. Go to `/user/profile/` - Upload profile picture
3. View storage indicators - Demonstrate S3 vs Local badges
4. Test file uploads - Show different file types
5. Check team features - Verify messaging and auth still work

---

## 📞 Support

For questions about S3 setup or implementation details, refer to:
- [Django Storages Documentation](https://django-storages.readthedocs.io/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
