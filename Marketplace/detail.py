class ListingDetailView(DetailView):
    model = Listing
    template_name = "marketplace/detail.html"
    context_object_name = "item"
