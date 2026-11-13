from django.urls import path

from . import views

app_name = "offers"

urlpatterns = [
    path("", views.offer_list, name="list"),
    path("offers/<int:offer_id>/", views.offer_detail, name="detail"),
    path("offers/new/", views.offer_create, name="create"),
    path(
    "offers/<int:offer_id>/request/",
    views.request_create,
    name="request_create",
),
path("requests/", views.request_list, name="requests"),
path(
    "requests/<int:request_id>/update/",
    views.request_update,
    name="request_update",
),
path(
    "requests/<int:request_id>/review/",
    views.review_create,
    name="review_create",
),
path("offers/<int:offer_id>/edit/", views.offer_edit, name="edit"),
path("offers/<int:offer_id>/hide/", views.offer_hide, name="hide"),
]
