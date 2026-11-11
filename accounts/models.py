from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    bio = models.TextField(blank=True)
    location_or_timezone = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Profile for {self.user.username}"

class SkillWanted(models.Model):
    profile = models.ForeignKey(
        Profile,
        on_delete=models.CASCADE,
        related_name="skills_wanted",
    )
    skill_name = models.CharField(max_length=100)

    class Meta:
        ordering = ["skill_name"]

    def __str__(self):
        return f"{self.skill_name} — {self.profile.user.username}"