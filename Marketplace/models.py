# Marketplace/models.py
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Listing(models.Model):
    CATEGORY_CHOICES = [
        ("furniture", "Furniture"),
        ("electronics", "Electronics"),
        ("textbooks", "Textbooks"),
        ("clothing", "Clothing"),
        ("donation", "Donation/Free"),
        ("other", "Other"),
    ]

    STATUS_CHOICES = [
        ("available", "Available"),
        ("sold", "Sold"),
        ("pending", "Pending"),
    ]

    

    title = models.CharField(max_length=120)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
    )
    pickup_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specify a safe pickup location for exchanges (e.g., 'UVA Library', 'Student Union')"
    )

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} ({self.seller})"


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="listing_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.listing.title}"
