from rest_framework import serializers

from apps.project.models import Project, ProjectImages
from apps.partner.models import Partner


class PartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partner
        fields = ["id", "name", "name_ar"]  # Adjust fields as needed


class ProjectImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProjectImages
        fields = "__all__"


class ProjectSerializer(serializers.ModelSerializer):
    gallery = ProjectImageSerializer(many=True, read_only=True, required=False)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(
            max_length=1000000, allow_empty_file=False, use_url=False
        ),
        write_only=True,
        required=False,
    )
    created_at = serializers.SerializerMethodField()
    created_by_user_name = serializers.CharField(
        source="created_by.name", read_only=True
    )
    created_by_user_name_ar = serializers.CharField(
        source="created_by.name_ar", read_only=True
    )
    updated_at = serializers.SerializerMethodField()
    updated_by_user_name = serializers.CharField(
        source="updated_by.name", read_only=True
    )
    updated_by_user_name_ar = serializers.CharField(
        source="updated_by.name_ar", read_only=True
    )
    partner_name=serializers.CharField(source= 'partner.name',read_only=True)
    partner_name_ar=serializers.CharField(source= 'partner.name_ar',read_only=True)
    class Meta:
        model = Project
        fields = [
            "id",
            "name",
            "name_ar",
            "description",
            "partner",
            "partner_name",
            "partner_name_ar",
            "created_at",
            "updated_at",
            "created_by",
            "created_by_user_name",
            "created_by_user_name_ar",
            "updated_by",
            "updated_by_user_name",
            "updated_by_user_name_ar",
            "is_active",
            "image",
            "gallery",
            "uploaded_images",

        ]
        read_only_fields = ["id"]

    def get_created_at(self, obj):
        return obj.created_at.strftime("%Y-%m-%d")

    def get_updated_at(self, obj):
        return obj.updated_at.strftime("%Y-%m-%d")

    def create(self, validated_data):
        uploaded_images_data = validated_data.pop(
            "uploaded_images", None
        )  # Extract uploaded images data

        project = Project.objects.create(**validated_data)  # Create the project object

        if uploaded_images_data:
            for image_data in uploaded_images_data:
                project_image = ProjectImages.objects.create(
                    project=project, image=image_data
                )  # Set project field
                project.gallery.add(
                    project_image
                )  # Associate project image with the project

        return project

    def update(self, instance, validated_data):
        uploaded_images_data = validated_data.pop("uploaded_images", None)

        # Update instance attributes with validated data
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()

        # Handle updating images
        if uploaded_images_data:
            # Delete existing images
            # instance.gallery.all().delete()

            # Create new images
            for image_data in uploaded_images_data:
                project_image = ProjectImages.objects.create(
                    project=instance, image=image_data
                )
                instance.gallery.add(project_image)

        return instance


class ProjectActiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["is_active"]


class ProjectDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["is_deleted"]


class ProjectDialogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "name_ar"]
