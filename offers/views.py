from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .models import Offer


def offer_list(request):
    query = request.GET.get("q", "").strip()

    offers = Offer.objects.filter(is_active=True).select_related("owner")

    if query:
        offers = offers.filter(
            Q(skill_name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__icontains=query)
        )

    return render(
        request,
        "offers/offer_list.html",
        {"offers": offers, "query": query},
    )

# Keep your existing offer_list function.

def offer_detail(request, offer_id):
    offer = get_object_or_404(
        Offer.objects.select_related("owner"),
        id=offer_id,
        is_active=True,
    )
    return render(request, "offers/offer_detail.html", {"offer": offer})
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import OfferForm


@login_required
def offer_create(request):
    if request.method == "POST":
        form = OfferForm(request.POST)

        if form.is_valid():
            offer = form.save(commit=False)
            offer.owner = request.user
            offer.save()
            return redirect("offers:detail", offer_id=offer.id)
    else:
        form = OfferForm()

    return render(request, "offers/offer_form.html", {"form": form})
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import OfferForm, SwapRequestForm
from .models import Offer, SwapRequest
@login_required
def request_create(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, is_active=True)

    if offer.owner_id == request.user.id:
        messages.error(request, "You cannot request your own offer.")
        return redirect("offers:detail", offer_id=offer.id)

    if request.method == "POST":
        form = SwapRequestForm(request.POST)

        if form.is_valid():
            swap_request = form.save(commit=False)
            swap_request.offer = offer
            swap_request.requester = request.user
            swap_request.save()

            messages.success(request, "Your request was sent.")
            return redirect("offers:detail", offer_id=offer.id)
    else:
        form = SwapRequestForm()

    return render(
        request,
        "offers/request_form.html",
        {"form": form, "offer": offer},
    )
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
@login_required
def request_list(request):
    sent = SwapRequest.objects.filter(
        requester=request.user
    ).select_related("offer", "offer__owner")

    received = SwapRequest.objects.filter(
        offer__owner=request.user
    ).select_related("offer", "requester")

    return render(
        request,
        "offers/request_list.html",
        {"sent": sent, "received": received},
    )


@login_required
@require_POST
def request_update(request, request_id):
    swap_request = get_object_or_404(SwapRequest, id=request_id)
    action = request.POST.get("action")

    if (
        action in ["accept", "decline"]
        and swap_request.offer.owner_id == request.user.id
        and swap_request.status == SwapRequest.Status.PENDING
    ):
        swap_request.status = (
            SwapRequest.Status.ACCEPTED
            if action == "accept"
            else SwapRequest.Status.DECLINED
        )

    elif (
        action == "cancel"
        and swap_request.requester_id == request.user.id
        and swap_request.status == SwapRequest.Status.PENDING
    ):
        swap_request.status = SwapRequest.Status.CANCELLED

    else:
        return HttpResponseForbidden("You can’t perform that action.")

    swap_request.save(update_fields=["status"])
    return redirect("offers:requests")