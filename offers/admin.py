from django.contrib import admin
from .models import Offer


@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ("skill_name", "owner", "category", "format", "is_active")
    list_filter = ("category", "format", "is_active")
    search_fields = ("skill_name", "description", "owner__username")