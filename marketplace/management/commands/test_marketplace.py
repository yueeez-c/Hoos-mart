"""
Management command to test database connections and S3 integration
"""
from django.core.management.base import BaseCommand
from django.db import connections
from marketplace.models import Listing, ListingImage
from django.conf import settings


class Command(BaseCommand):
    help = 'Test database connections and S3 integration for marketplace'

    def add_arguments(self, parser):
        parser.add_argument(
            '--check-db',
            action='store_true',
            help='Check database connection status',
        )
        parser.add_argument(
            '--check-s3',
            action='store_true',
            help='Check S3 configuration',
        )
        parser.add_argument(
            '--test-queries',
            action='store_true',
            help='Test marketplace queries',
        )

    def handle(self, *args, **options):
        if options['check_db']:
            self.check_database()
        
        if options['check_s3']:
            self.check_s3_config()
        
        if options['test_queries']:
            self.test_marketplace_queries()

    def check_database(self):
        """Check database connection status"""
        self.stdout.write("Checking database connections...")
        
        for alias in connections:
            try:
                connection = connections[alias]
                connection.ensure_connection()
                self.stdout.write(
                    self.style.SUCCESS(f'✓ Database connection "{alias}" is working')
                )
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'✗ Database connection "{alias}" failed: {e}')
                )

    def check_s3_config(self):
        """Check S3 configuration"""
        self.stdout.write("Checking S3 configuration...")
        
        s3_settings = {
            'AWS_ACCESS_KEY_ID': getattr(settings, 'AWS_ACCESS_KEY_ID', None),
            'AWS_SECRET_ACCESS_KEY': bool(getattr(settings, 'AWS_SECRET_ACCESS_KEY', None)),
            'AWS_STORAGE_BUCKET_NAME': getattr(settings, 'AWS_STORAGE_BUCKET_NAME', None),
            'AWS_S3_REGION_NAME': getattr(settings, 'AWS_S3_REGION_NAME', None),
            'DEFAULT_FILE_STORAGE': getattr(settings, 'DEFAULT_FILE_STORAGE', None),
        }
        
        for key, value in s3_settings.items():
            if key == 'AWS_SECRET_ACCESS_KEY':
                status = "Set" if value else "Not set"
                self.stdout.write(f"{key}: {status}")
            else:
                self.stdout.write(f"{key}: {value}")

    def test_marketplace_queries(self):
        """Test marketplace queries"""
        self.stdout.write("Testing marketplace queries...")
        
        try:
            # Test basic listing query
            listing_count = Listing.objects.count()
            self.stdout.write(f"Total listings: {listing_count}")
            
            # Test optimized query
            listings_with_images = Listing.objects.select_related('seller').prefetch_related('images')[:5]
            self.stdout.write(f"Successfully queried {len(listings_with_images)} listings with optimization")
            
            # Test image queries
            image_count = ListingImage.objects.count()
            self.stdout.write(f"Total images: {image_count}")
            
            self.stdout.write(self.style.SUCCESS("✓ All marketplace queries working"))
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'✗ Marketplace query failed: {e}')
            )