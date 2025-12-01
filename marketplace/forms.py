from django import forms
from .models import Listing


class MultipleFileInput(forms.ClearableFileInput):
    # this is the key line ✅
    allow_multiple_selected = True


class ListingCreateForm(forms.ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "price", "category", "status", "pickup_location"]
        widgets = {
            'pickup_location': forms.TextInput(attrs={
                'placeholder': 'e.g., UVA Library, Student Union, etc.',
                'class': 'form-control'
            })
        }

class ListingSearchForm(forms.Form):
    SORT_CHOICES = [
        ("", "Newest"),
        ("price_asc", "Price: Low → High"),
        ("price_desc", "Price: High → Low"),
        ("title_asc", "Title A→Z"),
    ]

    q = forms.CharField(
        label="Search",
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "Search listings...", "class": "form-control"})
    )

    # Pull choices from your model; add a blank choice at the top
    category = forms.ChoiceField(
        label="Category",
        required=False,
        choices=[("", "All categories")] + list(getattr(Listing, "CATEGORY_CHOICES", [])),
        widget=forms.Select(attrs={"class": "form-select"})
    )

    min_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Min"})
    )
    max_price = forms.DecimalField(
        required=False, min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control", "placeholder": "Max"})
    )

    # Optional: only if you have a condition choices field on Listing
    if hasattr(Listing, "CONDITION_CHOICES"):
        condition = forms.ChoiceField(
            label="Condition",
            required=False,
            choices=[("", "Any condition")] + list(getattr(Listing, "CONDITION_CHOICES", [])),
            widget=forms.Select(attrs={"class": "form-select"})
        )

    sort = forms.ChoiceField(
        label="Sort by",
        required=False,
        choices= SORT_CHOICES,
        widget=forms.Select(attrs={"class": "form-select"})
    )