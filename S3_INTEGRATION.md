# Amazon S3 File Storage Setup

## Overview
This setup enables file upload and storage with Amazon S3 for your Django application. This integrates with the existing messaging system and user profiles.

## Features
- **Automatic S3 Integration**: All file uploads go directly to S3
- **Works with Messaging**: File attachments in messages stored in S3
- **Profile Pictures**: User profile images stored in S3
- **Environment-based Configuration**: Easy switching between local and S3 storage

## AWS S3 Setup

### 1. Create S3 Bucket
The bucket name is configured as `project-b-17-media-files` in the environment variables.

1. Go to AWS S3 Console
2. Click "Create bucket"
3. Bucket name: `project-b-17-media-files`
4. Region: `us-east-1`
5. Keep default settings

### 2. AWS Credentials
Your AWS credentials are already configured in the `.env` file:
- **Access Key ID**: `AKIA5ODZ65YM1GGJAFYG`
- **Secret Access Key**: Already set

## Configuration

### S3 Settings (Already Configured)
The following settings are integrated with the team's code:

```python
# AWS S3 Configuration
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-east-1')

# Media files configuration
if AWS_STORAGE_BUCKET_NAME:
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
else:
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    MEDIA_URL = '/media/'
```

## Integration with Team Features

### Messaging System
- File attachments in messages automatically upload to S3
- Files are organized by conversation ID
- Secure download through Django views

### User Profiles  
- Profile pictures stored in S3
- Google authentication profile images cached in S3

### File Organization in S3
```
project-b-17-media-files/
├── media/
│   ├── profile_pics/
│   │   └── user_avatars.jpg
│   ├── message_files/
│   │   └── attachments.pdf
│   └── uploads/
│       └── various_files.*
```

## Testing S3 Integration

1. **Create S3 bucket**: `project-b-17-media-files`
2. **Upload a profile picture** through user profile
3. **Send a file in messaging** 
4. **Check S3 console** to see files uploaded

## Environment Variables
Already configured in `.env`:
```
AWS_ACCESS_KEY_ID=AKIA5ODZ65YM1GGJAFYG
AWS_SECRET_ACCESS_KEY=[configured]
AWS_STORAGE_BUCKET_NAME=project-b-17-media-files
AWS_S3_REGION_NAME=us-east-1
```

## Security
- `.env` file is in `.gitignore`
- AWS credentials not committed to repository
- Files served through secure HTTPS URLs