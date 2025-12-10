import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from marketplace.models import Listing, ListingImage
from decimal import Decimal
from django.utils import timezone

User = get_user_model()

print('Starting marketplace data sync...')

# Delete existing data
print('Deleting existing marketplace data...')
ListingImage.objects.all().delete()
Listing.objects.all().delete()
print('Deleted existing data')

# Get the seller
try:
    seller = User.objects.get(id=1)
except User.DoesNotExist:
    seller = User.objects.first()

print(f'Using seller: {seller.username}')

# Create listings
print('Creating listings...')

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

print(f'Created listing: {couch.title}')
print(f'Created listing: {tv.title}')

# Create images
print('Creating image references...')

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

print('Created image references')
print(f'Sync complete! Listings: {Listing.objects.count()}, Images: {ListingImage.objects.count()}')
print('NOTE: Make sure the actual image files exist in your S3 bucket!')
