"""
Custom storage backends for S3 with better connection handling
"""
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
import boto3
from botocore.config import Config


class OptimizedS3Boto3Storage(S3Boto3Storage):
    """
    S3 storage with optimized connection pooling and retry logic
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure connection pooling and retry logic
        self._config = Config(
            region_name=getattr(settings, 'AWS_S3_REGION_NAME', 'us-east-1'),
            retries={
                'max_attempts': getattr(settings, 'AWS_S3_RETRIES', {}).get('max_attempts', 3),
                'mode': getattr(settings, 'AWS_S3_RETRIES', {}).get('mode', 'adaptive')
            },
            max_pool_connections=getattr(settings, 'AWS_S3_MAX_POOL_CONNECTIONS', 50),
            # Add timeout configurations
            connect_timeout=60,
            read_timeout=60,
        )
    
    def _get_config_params(self):
        """Override to include our custom config"""
        config_params = super()._get_config_params()
        config_params['config'] = self._config
        return config_params


class MediaStorage(OptimizedS3Boto3Storage):
    """Custom media files storage"""
    location = 'media'
    default_acl = None
    file_overwrite = False
    custom_domain = False  # Use the S3 URL directly