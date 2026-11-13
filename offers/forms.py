from django import forms

from .models import Offer, Review, SwapRequest


class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = [
            "skill_name",
            "category",
            "description",
            "format",
            "availability_notes",
        ]


class SwapRequestForm(forms.ModelForm):
    class Meta:
        model = SwapRequest
        fields = ["message"]


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ["rating", "comment"]