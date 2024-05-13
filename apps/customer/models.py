from user.models import User
from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile
from django.utils.translation import gettext_lazy as _

import uuid
import os
from PIL import Image
from io import BytesIO


class Customer(User):
    is_customer = models.BooleanField(default=True)

    # def set_is_staff(self, is_staff):
    #     self.is_staff = False
    #     self.save()
    def set_is_staff(self, is_staff):
        self.user.is_staff = is_staff
        self.user.save()

    def validate_unique(self, exclude=None):
        super().validate_unique(exclude)
        if self.user.email and User.objects.filter(email=self.user.email).exists():
            raise models.ValidationError(
                {
                    "user": _(
                        "This email address is already associated with another user."
                    )
                }
            )
