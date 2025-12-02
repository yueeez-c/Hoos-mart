from django.shortcuts import render
from django.http import HttpResponse
from .models import Post
from marketplace.models import Listing

def home(request):
    listings = (
        Listing.objects
        .filter(status="available")
        .order_by('-id')[:5]   # or '-created_at' if you have that
    )

    print("HOME VIEW LISTING COUNT:", listings.count())

    context = {
        "recent_listings": listings,   # 👈 match the template variable name
    }
    return render(request, "home/home.html", context)



def about(request):
    return render(request, 'home/about.html')
