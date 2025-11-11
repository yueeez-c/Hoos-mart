from django import forms
from .models import Listing


class MultipleFileInput(forms.ClearableFileInput):
    # this is the key line ✅
    allow_multiple_selected = True


class ListingCreateForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={"multiple": True}),
        required=False,
        label="Item photos",
    )

    class Meta:
        model = Listing
        exclude = ["seller"]
        fields = ["title", "description", "price", "category",  "status"] #add 
