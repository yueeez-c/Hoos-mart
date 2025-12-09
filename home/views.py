from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from marketplace.models import Listing

def home(request):
    # Optimize database query to prevent connection exhaustion
    listings = (
        Listing.objects
        .select_related('seller')  # Prevent N+1 queries for seller info
        .prefetch_related('images')  # Prevent N+1 queries for images
        .filter(status="available", is_active=True)
        .order_by('-created_at')[:5]  # Use created_at for better performance with index
    )

    # Don't use .count() as it triggers additional query - use len() on sliced queryset
    print("HOME VIEW LISTING COUNT:", len(list(listings)))

    context = {
        "recent_listings": listings,
    }
    return render(request, "home/home.html", context)



def about(request):
    return render(request, 'home/about.html')
