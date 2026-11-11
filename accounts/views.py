from django.contrib.auth import get_user_model
from offers.models import Offer
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from .forms import ProfileForm, SkillWantedForm
from .models import Profile, SkillWanted


class SignUpView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy("login")


@login_required
def profile_edit(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)

        if form.is_valid():
            form.save()
            messages.success(request, "Your profile was saved.")
            return redirect("accounts:profile_edit")
    else:
        form = ProfileForm(instance=profile)

    return render(
        request,
        "accounts/profile_form.html",
        {
            "form": form,
            "skill_form": SkillWantedForm(),
            "wanted_skills": profile.skills_wanted.all(),
        },
    )


@login_required
@require_POST
def skill_wanted_add(request):
    profile, _ = Profile.objects.get_or_create(user=request.user)
    form = SkillWantedForm(request.POST)

    if form.is_valid():
        skill = form.save(commit=False)
        skill.profile = profile
        skill.save()

    return redirect("accounts:profile_edit")


@login_required
@require_POST
def skill_wanted_delete(request, skill_id):
    skill = get_object_or_404(
        SkillWanted,
        id=skill_id,
        profile__user=request.user,
    )
    skill.delete()
    return redirect("accounts:profile_edit")

def profile_detail(request, username):
    member = get_object_or_404(get_user_model(), username=username)
    profile = Profile.objects.filter(user=member).first()

    wanted_skills = (
        profile.skills_wanted.all()
        if profile
        else []
    )

    offers = Offer.objects.filter(owner=member, is_active=True)

    return render(
        request,
        "accounts/profile_detail.html",
        {
            "member": member,
            "profile": profile,
            "wanted_skills": wanted_skills,
            "offers": offers,
        },
    )