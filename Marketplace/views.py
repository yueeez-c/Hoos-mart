# Marketplace/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from .forms import ListingCreateForm, ListingSearchForm
from .models import Listing, ListingImage

  
def buy_marketplace(request):
    qs = Listing.objects.all()

    form = ListingSearchForm(request.GET or None)
    if form.is_valid():
        q         = form.cleaned_data.get("q") or ""
        category  = form.cleaned_data.get("category") or ""
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        sort      = form.cleaned_data.get("sort") or ""
        condition = form.cleaned_data.get("condition")  # may be None

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        if category:
            qs = qs.filter(category=category)
        if condition:
            qs = qs.filter(condition=condition)
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        if sort == "price_asc":
            qs = qs.order_by("price", "-id")
        elif sort == "price_desc":
            qs = qs.order_by("-price", "-id")
        elif sort == "title_asc":
            qs = qs.order_by("title")
        else:
            qs = qs.order_by("-id")

    return render(request, "marketplace/list.html", {"form": form, "listings": qs})

def listing_list(request):
    qs = Listing.objects.all()

    # Only show available/active listings if you have such fields
    if hasattr(Listing, "is_active"):
        qs = qs.filter(is_active=True)
    if hasattr(Listing, "is_sold"):
        qs = qs.filter(is_sold=False)

    form = ListingSearchForm(request.GET or None)
    if form.is_valid():
        q         = form.cleaned_data.get("q") or ""
        category  = form.cleaned_data.get("category") or ""
        min_price = form.cleaned_data.get("min_price")
        max_price = form.cleaned_data.get("max_price")
        sort      = form.cleaned_data.get("sort") or ""

        # Optional condition if present on model
        condition = form.cleaned_data.get("condition") if "condition" in form.fields else ""

        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))

        if category:
            qs = qs.filter(category=category)

        if condition:
            qs = qs.filter(condition=condition)

        if min_price is not None:
            qs = qs.filter(price__gte=min_price)

        if max_price is not None:
            qs = qs.filter(price__lte=max_price)

        if sort == "price_asc":
            qs = qs.order_by("price", "-id")
        elif sort == "price_desc":
            qs = qs.order_by("-price", "-id")
        elif sort == "title_asc":
            qs = qs.order_by("title")
        else:
            # default newest first
            order_field = "-created_at" if hasattr(Listing, "created_at") else "-id"
            qs = qs.order_by(order_field)

    # paginate
    paginator = Paginator(qs, 12)  # 12 cards per page
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(request, "marketplace/list.html", {
        "form": form,
        "page_obj": page_obj,
        "object_list": page_obj.object_list,
        "querystring": request.GET.urlencode(),
    })

def listing_detail(request, pk):
    listing = get_object_or_404(Listing.objects.prefetch_related("images"), pk=pk)
    return render(request, "marketplace/detail.html", {"listing": listing})

@login_required
def sell_marketplace(request):
    if request.method == "POST":
        # IMPORTANT: pass request.FILES
        form = ListingCreateForm(request.POST, request.FILES)
        if form.is_valid():
            # Save the listing first
            listing = form.save(commit=False)
            listing.seller = request.user
            listing.save()

            # Save each uploaded image as a ListingImage
            # NOTE: "images" must match the name of the FileField in your form
            for uploaded_file in request.FILES.getlist("images"):
                ListingImage.objects.create(
                    listing=listing,
                    image=uploaded_file,
                )

            messages.success(request, "Listing created!")
            return redirect("marketplace-sell")
    else:
        form = ListingCreateForm()

    user_listings = Listing.objects.filter(
        seller=request.user
    ).order_by("-created_at")

    return render(
        request,
        "marketplace/sell.html",
        {"form": form, "user_listings": user_listings},
    )


@login_required
def edit_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)

    if request.method == "POST":
        form = ListingCreateForm(request.POST, request.FILES, instance=listing)
        if form.is_valid():
            form.save()
            messages.success(request, "Listing updated.")
            return redirect("marketplace-sell")  # back to your “sell” page
    else:
        form = ListingCreateForm(instance=listing)

    return render(
        request,
        "marketplace/edit_listing.html",
        {"form": form, "listing": listing},
    )

@login_required
@require_POST
def delete_listing(request, pk):
    listing = get_object_or_404(Listing, pk=pk, seller=request.user)
    listing.delete()
    messages.success(request, "Listing deleted.")
    return redirect("marketplace-sell")


def listing_detail(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    return render(request, "marketplace/detail.html", {"listing": listing})
