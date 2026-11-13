from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import OfferForm, ReviewForm, SwapRequestForm
from .models import Offer, Review, SwapRequest


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


def offer_detail(request, offer_id):
    offer = get_object_or_404(
        Offer.objects.select_related("owner"),
        id=offer_id,
        is_active=True,
    )
    return render(request, "offers/offer_detail.html", {"offer": offer})


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

    return render(
        request,
        "offers/offer_form.html",
        {
            "form": form,
            "page_title": "Post a skill",
            "button_label": "Post offer",
        },
    )


@login_required
def offer_edit(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, owner=request.user)

    if request.method == "POST":
        form = OfferForm(request.POST, instance=offer)
        if form.is_valid():
            form.save()
            messages.success(request, "Your offer was updated.")
            return redirect("offers:detail", offer_id=offer.id)
    else:
        form = OfferForm(instance=offer)

    return render(
        request,
        "offers/offer_form.html",
        {
            "form": form,
            "page_title": "Edit your offer",
            "button_label": "Save changes",
        },
    )


@login_required
def offer_hide(request, offer_id):
    offer = get_object_or_404(Offer, id=offer_id, owner=request.user)

    if request.method == "POST":
        offer.is_active = False
        offer.save(update_fields=["is_active"])
        messages.success(request, "Your offer is no longer listed.")
        return redirect("offers:list")

    return render(request, "offers/offer_confirm_hide.html", {"offer": offer})


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
    elif (
        action == "complete"
        and request.user.id
        in [swap_request.offer.owner_id, swap_request.requester_id]
        and swap_request.status == SwapRequest.Status.ACCEPTED
    ):
        swap_request.status = SwapRequest.Status.COMPLETED
    else:
        return HttpResponseForbidden("You can’t perform that action.")

    swap_request.save(update_fields=["status"])
    return redirect("offers:requests")


@login_required
def review_create(request, request_id):
    swap_request = get_object_or_404(
        SwapRequest.objects.select_related("offer__owner", "requester"),
        id=request_id,
    )
    if swap_request.status != SwapRequest.Status.COMPLETED:
        return HttpResponseForbidden("Reviews are allowed after a swap is completed.")

    if swap_request.requester_id == request.user.id:
        reviewee = swap_request.offer.owner
    elif swap_request.offer.owner_id == request.user.id:
        reviewee = swap_request.requester
    else:
        return HttpResponseForbidden("Only swap participants can leave a review.")

    already_reviewed = Review.objects.filter(
        swap_request=swap_request,
        reviewer=request.user,
    ).exists()
    if already_reviewed:
        messages.info(request, "You already reviewed this swap.")
        return redirect("offers:requests")

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.swap_request = swap_request
            review.reviewer = request.user
            review.reviewee = reviewee
            review.save()
            messages.success(request, "Your review was saved.")
            return redirect("offers:requests")
    else:
        form = ReviewForm()

    return render(
        request,
        "offers/review_form.html",
        {"form": form, "swap_request": swap_request, "reviewee": reviewee},
    )
