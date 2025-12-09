# marketplace/models.py
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

    title = models.CharField(max_length=120, db_index=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2, db_index=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, db_index=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="available",
        db_index=True,
    )
    pickup_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Specify a safe pickup location for exchanges (e.g., 'UVA Library', 'Student Union')"
    )

    seller = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listings", db_index=True
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['is_active', 'status', '-created_at']),
            models.Index(fields=['seller', '-created_at']),
            models.Index(fields=['category', 'is_active']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.seller})"


class ListingImage(models.Model):
    listing = models.ForeignKey(
        Listing, on_delete=models.CASCADE, related_name="images", db_index=True
    )
    image = models.ImageField(upload_to="listing_images/")
    uploaded_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        indexes = [
            models.Index(fields=['listing', '-uploaded_at']),
        ]
        ordering = ['uploaded_at']

    def __str__(self):
        return f"Image for {self.listing.title}"
