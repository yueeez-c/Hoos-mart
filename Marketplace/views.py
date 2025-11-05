# Marketplace/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404

from .forms import ListingCreateForm
from .models import Listing, ListingImage


def buy_marketplace(request):
    """
    Buyer-facing marketplace page:
    - shows all listings
    - optional search and category filter via GET params
    """
    listings = Listing.objects.all().order_by("-created_at")

    search = request.GET.get("q")
    category = request.GET.get("category")

    if search:
        listings = listings.filter(title__icontains=search)

    if category:
        listings = listings.filter(category=category)

    return render(request, "marketplace/list.html", {"listings": listings})


@login_required
def sell_marketplace(request):
    """
    Seller-facing page:
    - form to create a new listing
    - list of this user's existing listings
    """
    if request.method == "POST":
        form = ListingCreateForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # handle multiple images
            for img in request.FILES.getlist("images"):
                ListingImage.objects.create(listing=listing, image=img)

            return redirect("marketplace-sell")
    else:
        form = ListingCreateForm()

    user_listings = Listing.objects.filter(seller=request.user).order_by("-created_at")

    return render(
        request,
        "marketplace/sell.html",
        {"form": form, "user_listings": user_listings},
    )


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "marketplace/detail.html", {"listing": listing})
