from django.db import models
from django.conf import settings

import uuid


class AboutUs(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    our_vision = models.TextField(null=True, blank=True)
    our_vision_ar = models.TextField(null=True, blank=True)
    our_mission = models.TextField(null=True, blank=True)
    our_mission_ar = models.TextField(null=True, blank=True)
    who_we_are = models.TextField(null=True, blank=True)
    who_we_are_ar = models.TextField(null=True, blank=True)
    our_promise = models.TextField(null=True, blank=True)
    our_promise_ar = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_created_aboutUs",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_updated_aboutUs",
        blank=True,
        null=True,
    )
