from django.db import models
from django.conf import settings
from django.core.files.base import ContentFile

import uuid
import os
from PIL import Image
from io import BytesIO

def partner_image_file_path(instance, filename):
    ext = os.path.splitext(filename)[1]
    filename = f"{uuid.uuid4()}{ext}"
    return os.path.join("uploads", "partner", filename)


class Partner(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    name_ar = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True,blank=True)
    photo = models.ImageField(blank=True, null=True, upload_to=partner_image_file_path)
    avatar = models.ImageField(upload_to=partner_image_file_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_created_partner",
        blank=True,
        null=True,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="user_updated_partner",
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Check if the photo exists and its size exceeds the maximum allowed size
        if self.photo:
            photo_size = self.photo.size  # Size in bytes
            max_size_bytes = 1024 * 1024  # 1 MB

            if photo_size > max_size_bytes:
                # Resize the photo
                self.resize_photo()

            # Resize and save the avatar image
            if not self.avatar:
                self.resize_and_save_avatar()

    def resize_photo(self):
        # Set the maximum size in bytes (1 MB = 1024 * 1024 bytes)
        max_size_bytes = 1024 * 1024

        # Open the image using Pillow
        with Image.open(self.photo.path) as img:
            # Check the size of the image in bytes
            img_byte_array = BytesIO()
            img.save(img_byte_array, format=img.format)
            img_size_bytes = img_byte_array.tell()

            # If the image size exceeds the maximum size, resize it
            if img_size_bytes > max_size_bytes:
                # Calculate the scaling factor to resize the image
                scaling_factor = (max_size_bytes / img_size_bytes) ** 0.5
                new_width = int(img.width * scaling_factor)
                new_height = int(img.height * scaling_factor)

                # Resize the image
                resized_img = img.resize((new_width, new_height))

                # Save the resized image back to the photo field
                buffer = BytesIO()
                resized_img.save(buffer, format=img.format)
                self.photo.save(
                    os.path.basename(self.photo.name),
                    ContentFile(buffer.getvalue()),
                    save=True,
                )

    def resize_and_save_avatar(self):
        # Check if the photo field is not empty
        if self.photo:
            photo_path = self.photo.path

            # Check if the avatar field is not already set
            # if not self.avatar:
            # Open the image using Pillow
        with Image.open(photo_path) as img:
            # Resize the image (adjust the size as needed)
            resized_img = img.resize((300, 300))

            # Save the resized image as the avatar
            buffer = BytesIO()
            resized_img.save(buffer, format="PNG")
            self.avatar.save("avatar.png", ContentFile(buffer.getvalue()), save=True)
