from django.conf import settings
from django.db import models


class Offer(models.Model):
    class Format(models.TextChoices):
        ONLINE = "online", "Online"
        IN_PERSON = "in_person", "In person"
        EITHER = "either", "Either"

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    skill_name = models.CharField(max_length=100)
    category = models.CharField(max_length=60, blank=True)
    description = models.TextField()
    format = models.CharField(
        max_length=20,
        choices=Format.choices,
        default=Format.ONLINE,
    )
    availability_notes = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.skill_name} — {self.owner}"


from django.conf import settings
from django.db import models


class SwapRequest(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        DECLINED = "declined", "Declined"
        CANCELLED = "cancelled", "Cancelled"
        COMPLETED = "completed", "Completed"

    offer = models.ForeignKey(
        Offer,
        on_delete=models.CASCADE,
        related_name="swap_requests",
    )
    requester = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_swap_requests",
    )
    message = models.TextField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Request for {self.offer} from {self.requester}"
