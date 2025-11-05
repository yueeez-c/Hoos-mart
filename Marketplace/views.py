from django.shortcuts import render

def buy_marketplace(request):
    # later: show all listings not owned by the current user
    return render(request, "marketplace/buy.html")

def sell_marketplace(request):
    # later: show a form + the current user's listings
    return render(request, "marketplace/sell.html")
