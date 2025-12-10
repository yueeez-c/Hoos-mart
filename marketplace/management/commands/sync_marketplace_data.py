"""
Management command to sync marketplace data from local to production
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from marketplace.models import Listing, ListingImage
from decimal import Decimal
from django.utils import timezone

User = get_user_model()


class Command(BaseCommand):
    help = 'Sync marketplace data - replaces production data with local data structure'

    def handle(self, *args, **options):
        self.stdout.write('Starting marketplace data sync...')
        
        # Delete existing data
        self.stdout.write('Deleting existing marketplace data...')
        ListingImage.objects.all().delete()
        Listing.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('✓ Deleted existing data'))
        
        # Get the seller (assuming user ID 1 exists, adjust as needed)
        try:
            seller = User.objects.get(id=1)
        except User.DoesNotExist:
            seller = User.objects.first()
            if not seller:
                self.stdout.write(self.style.ERROR('No users found in database!'))
                return
        
        self.stdout.write(f'Using seller: {seller.username}')
        
        # Create listings
        self.stdout.write('Creating listings...')
        
        # Couch listing
        couch = Listing.objects.create(
            id=1,
            title="couch",
            description="Leather couch",
            price=Decimal("700.00"),
            category="furniture",
            status="available",
            pickup_location="Nau Hall",
            seller=seller,
            created_at=timezone.now(),
            is_active=True
        )
        
        # TV listing
        tv = Listing.objects.create(
            id=2,
            title="TV",
            description="New television",
            price=Decimal("400.00"),
            category="electronics",
            status="available",
            pickup_location="UVA Library",
            seller=seller,
            created_at=timezone.now(),
            is_active=True
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created listing: {couch.title}'))
        self.stdout.write(self.style.SUCCESS(f'✓ Created listing: {tv.title}'))
        
        # Create images (note: image files need to exist in S3)
        self.stdout.write('Creating image references...')
        
        ListingImage.objects.create(
            id=1,
            listing=couch,
            image="listing_images/images.jpg",
            uploaded_at=timezone.now()
        )
        
        ListingImage.objects.create(
            id=2,
            listing=tv,
            image="listing_images/TV.jpg",
            uploaded_at=timezone.now()
        )
        
        self.stdout.write(self.style.SUCCESS('✓ Created image references'))
        
        # Summary
        total_listings = Listing.objects.count()
        total_images = ListingImage.objects.count()
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ Sync complete!'))
        self.stdout.write(self.style.SUCCESS(f'  - Listings: {total_listings}'))
        self.stdout.write(self.style.SUCCESS(f'  - Images: {total_images}'))
        self.stdout.write(self.style.WARNING('\nNote: Make sure the actual image files exist in your S3 bucket!'))
