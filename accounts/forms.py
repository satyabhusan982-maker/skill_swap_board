from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["bio", "location_or_timezone"]
from .models import Profile, SkillWanted


class SkillWantedForm(forms.ModelForm):
    class Meta:
        model = SkillWanted
        fields = ["skill_name"]