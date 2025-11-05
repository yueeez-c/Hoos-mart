from django.urls import reverse_lazy
from django import forms

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "price", "description", "image"]  # add category if you have it

class ListingCreateView(LoginRequiredMixin, CreateView):
    model = Listing
    form_class = ListingForm
    template_name = "marketplace/form.html"
    success_url = reverse_lazy("marketplace")

    def form_valid(self, form):
        form.instance.seller = self.request.user
        return super().form_valid(form)
