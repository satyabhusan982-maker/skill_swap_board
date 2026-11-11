from django.urls import path

from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("profile/", views.profile_edit, name="profile_edit"),
    path("profile/skills/add/", views.skill_wanted_add, name="skill_wanted_add"),
path(
    "profile/skills/<int:skill_id>/delete/",
    views.skill_wanted_delete,
    name="skill_wanted_delete",
),
path(
    "members/<str:username>/",
    views.profile_detail,
    name="profile_detail",
),
]